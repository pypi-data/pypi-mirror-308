"""
Calibrates the gripper and saves the new motor offsets in motor_config.yaml.
"""

# Standard
import argparse

# Custom
import mimic_hand_middleware


def update_calibration_with_current_pose(
    calibration_path: str = 'git/mimic_hand_middleware/mimic_hand_middleware/motor_config.yaml',
):
    """
    Updates the calibration file at calibration_path with the current position of the
    finger joints as zero position.
    """
    print(f'Got calibration path: {calibration_path}')
    gripper_controller = mimic_hand_middleware.GripperController(
        calibrate_at_start=True, motor_config_yml_path=calibration_path
    )
    gripper_controller.disconnect_motors()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Calibrate the mimic hand's zero position."
    )
    parser.add_argument(
        'calib_yaml_path', type=str, help='Path to the calibration file'
    )
    args = parser.parse_args()
    mimic_hand_middleware.set_motors_to_freerunning_mode()
    input('Move motors to the new zero position, then press enter to save')
    update_calibration_with_current_pose(calibration_path=args.calib_yaml_path)
