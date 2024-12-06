"""Command joint angles on a mimic hand.

High level file providing access to the middleware of the hand prototypes from
P04 onwards. Its main class, GripperController, provides functions to set motor
operation modes (freerunning/position controlled), read and write motor angles,
and command joint angles. All angles are represented in degrees. Motor angles
are reset to zero in their current position at each power cycle, therefore a
calibration process is provided that resets these (TODO see README.md).

Made by Benedek Forrai (ben.forrai@mimicrobotics.com)
"""

# standard
import logging
import os
import time
from copy import deepcopy
from pathlib import Path
from threading import RLock

# third-party
import numpy as np
import yaml
from mimic_hand_api import RP2040API

# custom
from .conversion_utils import p04 as hand_utils
from .kinematics.hand_kinematics import HandKinematics


class GripperController:
    """Command joint-level functions on mimic's robotic hands.

    Middleware level class for controlling mimic's robotic hands for prototypes
    newer than P04.
    Provides the following methods for easier integration:
    - connect_to_motors: connects to the motors of the hand to the API
    - init_joints: "homes" the hands and starts the EKF tracking if specified.
    - command_joint_angles: sends the desired joint (!) angles to the hand. The
        hand then takes a motor configuration that is as close to the commanded
        joint angles as possible.
    - get_joint_pos: returns the current position of the joints (in deg.)
    - get_joint_vel: returns the speed of the joints (in deg./s)
    - get_motor_pos_vel_cur: returns the position (deg), rot. speed (deg/s) and
        current (mA) of the motors
    """

    def __init__(
        self: 'GripperController',
        prototype_name: str = 'p4',
        port: str = '/dev/mimic_hand_driver',
        config_yml: str = 'p_0_4.yaml',
        motor_config_yml_path: str = 'git/mimic_hand_middleware/mimic_hand_middleware/motor_config.yaml',
        init_motor_pos_update_thread: bool = True,
        use_sim_joint_measurement: bool = False,
        compliant_test_mode: bool = False,
        max_motor_current: float = 200.0,
        use_sim_motors: bool = False,
        calibrate_at_start: bool = False,
        motor_port_env_var: str = 'HAND_PORT',
        log_level: int = logging.DEBUG,
    ) -> None:
        """Initialize the GripperController object.

        The controller has the following parameters:
        - prototype_name (str): name of the hand prototype that is currently in
            use
        - port (str): name of the USB port to connect to
        - config_yml (str): name of config file defining the MuscleGroups in a
            hand. Legacy, kept only for backwards compatibility
        - init_motor_pos_update_thread (bool): legacy, kept only for
            compatibility
        - use_sim_joint_measurement (bool): whether to run the EKF tracker
        - compliant_test_mode (bool): legacy, kept only for compatibility
        (not back-driveable currently sadly)
        - max_motor_current (float): maximum allowed motor current in mA
        - use_sim_motors (bool): if set to true, run a virtual simple sim of
            the hand
        - calibrate_at_start (bool): if set to true, the initial position of the hand
        will be taken as the new zero position for the hand's motors.
        """
        # Init class variables
        self._prototype = prototype_name
        self._cfg_file_name = config_yml
        # check if motor config directory needs extension with home dir
        cfg_file_dir = Path(motor_config_yml_path).parents[0]
        if cfg_file_dir.is_dir():
            self._motor_cfg_file = Path(motor_config_yml_path)
        else:
            self._motor_cfg_file = Path('~/' + motor_config_yml_path).expanduser()
        self._init_pos_update = init_motor_pos_update_thread
        self._sim_measurement = use_sim_joint_measurement
        self._sim_motors = use_sim_motors
        self._compliant_mode_legacy = compliant_test_mode
        self._max_motor_current = max_motor_current
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)
        # Init port for hand communication
        if motor_port_env_var in os.environ:
            self._port = '/dev/' + str(os.environ[motor_port_env_var])
        else:
            self._port = port
        # Import/init low-level utilities
        self._hand_kinematics = HandKinematics(yaml_name=self._cfg_file_name)
        hand_utils.init_matrices()
        # Init constants
        self.num_of_joints = len(hand_utils.JOINT_NAMES_NORMAL)
        self.joint_names = hand_utils.JOINT_NAMES_NORMAL
        self.joint_limit_lower = hand_utils.GC_LIMITS_LOWER
        self.joint_limit_higher = hand_utils.GC_LIMITS_UPPER
        self.num_of_motors = len(hand_utils.MOTOR_NAMES)
        self._motor_zero_offsets = np.zeros((self.num_of_motors,))
        self.motors_limit_lower = hand_utils.MOTOR_LIMIT_LOWER
        self.motors_limit_higher = hand_utils.MOTOR_LIMIT_HIGHER
        self.motors_mcp_to_mean_delta = hand_utils.MCP_TO_MEAN_DELTA
        self.motors_mcp_from_mean_delta = hand_utils.MCP_FROM_MEAN_DELTA
        self.torque_enabled = False
        # Disable scientific notation for printing np arrays
        np.set_printoptions(suppress=True)
        if calibrate_at_start:
            self.connect_motors()
            self._driver_api.set_all_motors_to_freerunning_mode()
            self._calibrate_motor_angles()
        else:
            try:
                log_msg = f'Loading motor cfg: {self._motor_cfg_file}'
                self._logger.info(log_msg)
                with Path.open(self._motor_cfg_file) as motor_cfg_file:
                    self._motor_config = yaml.safe_load(motor_cfg_file)
                self._motor_zero_offsets = np.array(
                    self._motor_config['zero_offsets'],
                ).reshape((-1,))
                log_msg = f'Motor offsets: {self._motor_zero_offsets}'
                self._logger.debug(log_msg)
            except FileNotFoundError:
                self._logger.warning('Failed to find motor_config.yaml!')

    def connect_motors(self: 'GripperController') -> None:
        """Connect to the motors of the hand.

        Create the RP2040API object to handle motor communication.
        If self._sim_motors is True, or the _driver_api is already
        created, this function does not do anything.

        :return: None
        """
        if not self._sim_motors and not hasattr(self, '_driver_api'):
            self._driver_api = RP2040API(port_name=self._port)
            self._driver_api.connect_all_motors()
            self._driver_api.set_current_limit(self._max_motor_current)
        else:
            pass

    def disconnect_motors(self: 'GripperController') -> None:
        """Disconnect motors from all boards.

        Disconnect all motors from the driver_api object. If
        If self.sim_motors is True, or there is no _driver client
        to disconnect from, this function does not do anything.

        :return: None
        """
        if not self._sim_motors and hasattr(self, '_driver_api'):
            self._driver_api.disconnect_all_motor_boards()
            self._logger.info(
                'Disconnected all motors. Controller can be shut down now!'
            )
        else:
            pass

    def enable_torque(self: 'GripperController') -> None:
        """Enable motor torque on all motors.

        Sets the motors to current-limited positional control mode.
        Motors in this mode can be sent to positions and also can
        send data on their status (position, current).
        If self._sim_motors is True, this function only sets the
        value of self.torque_enabled to True.

        :return: None
        """
        if not self._sim_motors:
            self._driver_api.set_all_motors_to_cur_lim_pos_control_mode()
        self.torque_enabled = True

    def disable_torque(self: 'GripperController') -> None:
        """Set the motors to freerunning mode.

        This function disables the torque on all motors, so they
        are easily backdriveable. Motor angles and currents can
        still be read in this mode.

        :return: None
        """
        self._driver_api.set_all_motors_to_freerunning_mode()
        self.torque_enabled = False

    def init_joints(self: 'GripperController', calibrate: bool = False) -> None:
        """Initializes the internal buffers of the hand and "homes" it to its zero
        position.
        If calibrate is set to True, calibrates the hand by driving it to its
        limit positions and registering motor positions.

        :return: None
        """
        self._motor_lock = RLock()
        self._joint_value_lock = RLock()
        # set zero initial position
        with self._joint_value_lock:
            self._joint_array = np.zeros((self.num_of_joints,))
        if not self._sim_motors:
            if calibrate:
                self._calibrate_motor_angles()
                # enable torque again
                self.enable_torque()

    def _get_motor_angles_from_tendon_lengths(
        self: 'GripperController',
        commanded_lengths: np.ndarray,
    ) -> np.ndarray:
        """Get motor angles (uncalibrated) from free tendon lenghts.

        Simply divides all tendon lengths by the spool radius. Assumes
        uniform spool radius for all motors.

        :param commanded_lengths: Commanded lengths for each tendon in meters,
        represented as an `np.ndarray` of shape `(num_of_motors,)`.
        :type commanded_lengths: np.ndarray
        :return: Motor angles that achieve the desired tendon lengths, in radians.
        :rtype: np.ndarray
        """
        return commanded_lengths / self._hand_kinematics.spool_rad

    def command_joint_angles(
        self: 'GripperController',
        commanded_angles: np.ndarray,
        convert_from_degrees: bool = True,
    ) -> None:
        """Command joint angles to the robotic hand.

        Commands joint angle command_angles (in degrees) to the low level
        controller. If self._sim_motors is True, this only updates the current
        commanded joint array.

        :param commanded_angles: Joint angles to command, as an `np.ndarray`.
        :type commanded_angles: np.ndarray
        :param convert_from_degrees: Whether to convert `commanded_angles` from degrees
            to radians before sending, defaults to `True`.
        :type convert_from_degrees: bool, optional
        :return: None
        """
        commanded_angles = deepcopy(commanded_angles)
        commanded_angles = self._filter_joint_angle_limits(commanded_angles)
        if convert_from_degrees:
            commanded_angles *= np.pi / 180
        commanded_angles = commanded_angles.reshape((-1,))
        assert commanded_angles.shape[0] == self.num_of_joints, (
            'Incorrect command dimension; got commanded shape of'
            + f' {commanded_angles.shape} while number of joints is '
            + f'{self.num_of_joints}!'
        )
        if not self._sim_motors:
            free_tendon_lengths = self._get_tendon_lengths_from_angles(commanded_angles)
            raw_spool_angles = self._get_motor_angles_from_tendon_lengths(
                free_tendon_lengths,
            )
            self.command_motor_angles(
                commanded_angles=raw_spool_angles,
                convert_from_radians=True,
            )
        else:
            with self._joint_value_lock:
                self._joint_array = commanded_angles

    def _get_tendon_lengths_from_angles(
        self: 'GripperController', angles_rad: np.ndarray
    ) -> np.ndarray:
        """Get desired tendon lengths from the desired joint positions.

        Calculates the desired "free" (difference from normal pos.) tendon
        length (in meters) from the desire joint array (in radians).

        :param angles_rad: Commanded angle of each joint in radians,
        represented as an `np.ndarray` of shape `(num_of_joints,)`.
        :type angles_rad: np.ndarray
        :return: Desired tendon lengths in meters that achieve the desired
        joint positions.
        :rtype: np.ndarray
        """
        tendon_lengths = (
            self._hand_kinematics.get_tendon_lengths_m_from_joint_angles_rad(angles_rad)
        )
        return tendon_lengths

    def _get_calibrated_motor_angles(
        self: 'GripperController', raw_spool_angles: np.ndarray
    ) -> np.ndarray:
        """Apply calibration offset to motor angles.

        Takes uncalibrated motor angle commands (in radians) and shifts them
        with the zero positions measured during calibration.

        :param raw_spool_angles: Uncalibrated motor angles in radians.
        :type raw_spool_angles: np.ndarray
        :return: Calibrated motor angles in radians.
        :rtype: np.ndarray
        """
        motor_angles = raw_spool_angles + self._motor_zero_offsets
        return motor_angles

    def _filter_joint_angle_limits(
        self: 'GripperController', raw_joint_angles: np.ndarray
    ) -> np.ndarray:
        """Clip joint angles to stay within the joint limits.

        Filters raw_joint_angles (assumed to be in degrees) to stay inside the
        joint limits.

        :param raw_joint_angles: Raw joint angles in degrees.
        :type raw_joint_angles: np.ndarray
        :return: Clipped joint angles in degrees.
        :rtype: np.ndarray
        """
        filtered_joint_angles = np.clip(
            a=raw_joint_angles,
            a_min=self.joint_limit_lower,
            a_max=self.joint_limit_higher,
        )
        return filtered_joint_angles

    def command_motor_angles(
        self: 'GripperController',
        commanded_angles: np.ndarray,
        convert_from_radians: bool = False,
    ) -> None:
        """Command desired motor angles.

        Command desired motor angles by default in degrees, if convert_from_radians
        is set, then radians are expected. Shifts the desired angles with the
        calibration values, then sends the position command to the motor boards
        through the driver api.

        :param commanded_angles: Commanded motor angles either in degrees (default) or
        radians (if convert_from_radians is set).
        :type commanded_angles: np.ndarray
        :param convert_from_radians: Set to true if you'd like to command radians to
        the motors. The default (False) means degrees will be used.
        :type convert_from_radians: bool
        :return: None
        """
        cmd_angles = deepcopy(commanded_angles)
        if convert_from_radians:
            cmd_angles = np.rad2deg(cmd_angles)
        cmd_angles = self._get_calibrated_motor_angles(cmd_angles)
        self._driver_api.command_middleware_motor_position_array(cmd_angles)

    def get_joint_pos(self: 'GripperController', use_ekf: bool = False) -> np.ndarray:
        """Return the position of the joints of the hand in degrees.

        Returns the joint position array of the hand in degrees. By default,
        uses the commanded joint positions for now, TODO use EKF/proprioception.

        :param use_ekf: Use and extended kalman filter/proprioception to get the
        real joint positions instead of the commanded positions (default)
        :type use_ekf: bool
        :return: The joint positions in degrees.
        :rtype: np.ndarray
        """
        joint_array = np.zeros(self.num_of_joints)
        with self._joint_value_lock:
            joint_array = deepcopy(self._joint_array)
        return joint_array

    def get_joint_vel(self: 'GripperController') -> np.ndarray:
        """Return the joint velocities in degrees/s.

        For now, a dummy funtion that only returns zeros. TODO implement using
        muscle jacobians - does not need proprioception.

        :return: The joint angular velocities in degrees/s
        :rtype: np.ndarray.
        """
        if not self._sim_motors:
            # TODO later this needs to come from the jacobian
            joint_vel_array = np.zeros((self.num_of_joints, 1))
        else:
            joint_vel_array = np.zeros((self.num_of_joints, 1))
        return joint_vel_array

    def get_motor_pos_vel_cur(self: 'GripperController') -> list:
        """Return all relevant motor info.

        Returns the position (degrees), velocity (degrees/s) and current (mA)
        measured by the motors as a list of np.ndarrays, each of shape (num_motors,).

        :return: List of 3 np.ndarrays, containing motor position, velocity and current
        :rtype: list
        """
        motor_pos = np.zeros((self.num_of_motors,))
        motor_vel = np.zeros((self.num_of_motors,))
        motor_cur = np.zeros((self.num_of_motors,))
        if not self._sim_motors:
            motor_cur = self._driver_api.get_motor_currents()
            motor_pos = self._driver_api.get_motor_positions()
        return motor_pos, motor_vel, motor_cur

    def _calibrate_motor_group(
        self: 'GripperController',
        motor_group_idxes: np.ndarray,
        forward_max_current_mA: float,
        backward_max_current_mA: float,
        starting_resolution_deg: float = 5.0,
        resolution_refine_steps: int = 2,
        resolution_refine_scale: float = 5.0,
    ) -> list:
        """Calibrate a motor group by driving it to its limits in each direction.

        Moves the motors selected by motor_group_idxes (with the middleware
        convention, see README.md) to the joint limits in both directions,
        until the respective current limit (forward/backward_max_current_mA) is
        hit. Repeats the test of the limit with smaller steps than the starting
        step size (starting_resolution_deg), with each step cycle scaled by
        1/resolution_refine_scale.

        :param motor_group_idxes: Indices of the motors to be calibrated,
        following middleware convention.
        :type motor_group_idxes: np.ndarray
        :param forward_max_current_mA: Maximum current threshold in milliamps for
        moving motors in the forward direction.
        :type forward_max_current_mA: float
        :param backward_max_current_mA: Maximum current threshold in milliamps for
        moving motors in the backward direction.
        :type backward_max_current_mA: float
        :param starting_resolution_deg: Initial step size in degrees for motor movement
        (defaults to 5.0.)
        :type starting_resolution_deg: float, optional
        :param resolution_refine_steps: Number of refinement cycles to reduce step size
        (defaults to 2.)
        :type resolution_refine_steps: int, optional
        :param resolution_refine_scale: Factor by which the step size is divided in
        each refinement cycle, defaults to 5.0.
        :type resolution_refine_scale: float, optional
        :return: A list containing the forward and backward limit positions.
        :rtype: list
        """
        self._logger.info('Calibrating motor group idxes:', extra=motor_group_idxes)
        step_sizes = [
            starting_resolution_deg / (resolution_refine_scale**i)
            for i in range(resolution_refine_steps)
        ]
        # calibrate positive direction
        start_angles = np.zeros_like(motor_group_idxes)
        for step_size in step_sizes:
            self._drive_group_until_limit(
                motor_group_idxes,
                max_current_mA=forward_max_current_mA,
                step=step_size,
                start_angles=start_angles,
            )
            limit_pos = self._driver_api.get_motor_positions()
            start_angles = limit_pos[motor_group_idxes] * 0.75
            time.sleep(0.5)
        forward_limit_pos = limit_pos[motor_group_idxes]
        # calibrate negative direction
        start_angles = np.zeros_like(motor_group_idxes)
        self._driver_api.command_middleware_motor_position_array(
            middleware_cmd_array=np.zeros((self.num_of_motors,)),
        )
        # delay for currents to got back to normal
        time.sleep(0.5)
        for step_size in step_sizes:
            self._drive_group_until_limit(
                motor_group_idxes,
                max_current_mA=backward_max_current_mA,
                step=-step_size,
                start_angles=start_angles,
            )
            limit_pos = self._driver_api.get_motor_positions()
            start_angles = deepcopy(limit_pos[motor_group_idxes])
            start_angles *= 0.75
            time.sleep(0.5)
        backward_limit_pos = limit_pos[motor_group_idxes]
        return [forward_limit_pos, backward_limit_pos]

    def _drive_group_until_limit(
        self: 'GripperController',
        motor_group_idxes: np.ndarray,
        max_current_mA: float,
        step: float,
        start_angles: np.ndarray = None,
    ) -> None:
        """Move a motor group until a current limit is hit.

        Moves the motors selected by motor_group_idxes (with the middleware
        convention, see README.md) with step until max_current_mA is hit. Sends
        the rest of the motors to 0 deg.

        :param motor_group_idxes: Indices of the motors to drive, following middleware
        convention.
        :type motor_group_idxes: np.ndarray
        :param max_current_mA: Maximum allowable current in milliamps before stopping
        motor movement.
        :type max_current_mA: float
        :param step: Step size for motor movement.
        :type step: float
        :param start_angles: Initial angles for the specified motors, default: `None`.
        :type start_angles: np.ndarray, optional
        :return: None
        """
        # init start angle
        motor_group_idxes = motor_group_idxes.reshape(-1)
        cmd_array = np.zeros((self.num_of_motors,))
        if start_angles is not None:
            cmd_array[motor_group_idxes] = start_angles
        # drive motor group to limit from start angle
        driven_group_cmd_array = cmd_array[motor_group_idxes]
        motor_cur = self._driver_api.get_motor_currents()
        while np.any(motor_cur[motor_group_idxes] < max_current_mA):
            driven_group_cmd_array[motor_cur[motor_group_idxes] < max_current_mA] += (
                step
            )
            cmd_array[motor_group_idxes] = driven_group_cmd_array
            self._driver_api.command_middleware_motor_position_array(cmd_array)
            time.sleep(abs(0.02 * step))
            motor_cur = self._driver_api.get_motor_currents()
            self._logger.debug('Motor currents: ', motor_cur)

    def _calibrate_motor_angles(self: 'GripperController') -> None:
        """Read current motor positions and write them to file.

        Assumes that the current motor positions correspond to the "homed" joint
        configuration, and writes them to a yaml file. TODO (ben) document
        homed joint positions.

        :return: None
        """
        self.get_new_motor_zero_positions()
        motor_dict = self._get_motor_dict()
        with open(self._motor_cfg_file, 'w') as cfg_file:
            yaml.safe_dump(
                data=motor_dict,
                stream=cfg_file,
            )
            self._logger.info('Saved calibration results and applied calibration!')

    def _get_motor_dict(self: 'GripperController') -> dict:
        """Get a dict of offsets that can be written to a calibration file.

        Assembles a motor dict from the current state of the motors that
        we can write to a calibration file.

        :return: A motor dict containing zero offsets (and later possibly other
        variables)
        :rtype: dict
        """
        motor_zero_offsets = self._motor_zero_offsets
        motor_dict = {
            'zero_offsets': [float(offset) for offset in list(motor_zero_offsets)],
        }
        return motor_dict

    def get_new_motor_zero_positions(self: 'GripperController') -> None:
        """Recalibrate motor offsets.

        Recalibrates the offsets for the motors such that the current position
        will be treated as the new zero position during operation.

        :return: None
        """
        self._motor_zero_offsets = self._driver_api.get_motor_positions()
