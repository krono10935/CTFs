package frc.robot.commands.drivetrain;

import java.util.function.BooleanSupplier;

import org.littletonrobotics.junction.Logger;

import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.button.CommandXboxController;
import frc.robot.RobotContainer;
import frc.robot.subsystems.drivetrain.Drivetrain;
import frc.utils.AllianceFlipUtil;

/**
 * Base driving command for the drivetrain.
 *
 * <p>
 * Handles:
 * <ul>
 *     <li>Controller input processing</li>
 *     <li>Speed scaling (linear & angular)</li>
 *     <li>Deadband filtering</li>
 *     <li>Field-relative driving</li>
 * </ul>
 * </p>
 */
public class DriveCommand extends Command {

    public enum ControllerMode {
        NONE(1),
        BRAKE_EXPONENTIAL(0.5),
        STICKS_EXPONENTIAL(0.5),
        BOTH_EXPONENTIAL(0.5);

        public final double exponent;

        ControllerMode(double exponent) {
            this.exponent = exponent;
        }

        public double calculateTrigger(double value){
            if(this == STICKS_EXPONENTIAL) return value;

            Logger.recordOutput("DriveCommand/trigger value input", value);

            return calculateExponential(value, exponent);
        }

        public double calculateStick(double value){
            if(this == BRAKE_EXPONENTIAL) return value;

            return  calculateExponential(value, exponent);
        }

        private static double calculateExponential(double value, double exponential) {
            return Math.copySign(Math.pow(Math.abs(value), exponential), value);
        }
    }

    protected final Drivetrain drivetrain;
    protected final CommandXboxController controller;

    protected double MAX_LINEAR_SPEED;
    protected double MIN_LINEAR_SPEED;
    protected double MAX_ANGULAR_SPEED;
    protected double MIN_ANGULAR_SPEED;

    /**
     * Deadband threshold for controller inputs
     */
    protected static final double DEADBAND = 0.1;

    private static final ControllerMode CONTROLLER_MODE = ControllerMode.BRAKE_EXPONENTIAL;

    public DriveCommand(Drivetrain drivetrain, CommandXboxController controller) {
        this.drivetrain = drivetrain;
        this.controller = controller;

        addRequirements(drivetrain);


        MAX_LINEAR_SPEED = drivetrain.getConstants().SPEED_CONFIG.maxLinearSpeed();
        MIN_LINEAR_SPEED = drivetrain.getConstants().SPEED_CONFIG.minLinearSpeed();
        MAX_ANGULAR_SPEED = drivetrain.getConstants().MAX_ANGULAR_SPEED;
        MIN_ANGULAR_SPEED = drivetrain.getConstants().MIN_ANGULAR_SPEED;
    }

    /**
     * Calculates the field-relative reference angle.
     */
    protected Rotation2d angleFieldRelative() {
        return AllianceFlipUtil.apply(drivetrain.getGyroAngle());
    }

    @Override
    public void execute() {
        ChassisSpeeds speeds = getControllerInputs();

        drivetrain.driveWithoutPP(
                ChassisSpeeds.fromFieldRelativeSpeeds(
                        speeds.vxMetersPerSecond,
                        speeds.vyMetersPerSecond,
                        speeds.omegaRadiansPerSecond,
                        angleFieldRelative()
                )
        );
    }

    /**
     * Linear interpolation for speed scaling.
     *
     * @param value normalized input (0–1)
     * @return interpolated linear speed
     */
    private double interpolate(double value) {
        return MIN_LINEAR_SPEED + (MAX_LINEAR_SPEED - MIN_LINEAR_SPEED) * value;
    }

    /**
     * Angular interpolation for rotation scaling.
     *
     * @param value normalized input (0–1)
     * @return interpolated angular speed
     */
    private double angularInterpolate(double value) {
        return MIN_ANGULAR_SPEED + (MAX_ANGULAR_SPEED - MIN_ANGULAR_SPEED) * value;
    }

    /**
     * Applies deadband to joystick input.
     */
    protected static double deadband(double value) {
        return Math.abs(value) < DEADBAND ? 0 : value;
    }

    @Override
    public void end(boolean interrupted) {
        drivetrain.stop();
    }

    /**
     * Converts controller input into chassis speeds.
     */
    public ChassisSpeeds getControllerInputs() {

        double triggerValue = CONTROLLER_MODE.calculateTrigger(1 - controller.getRightTriggerAxis());

        double speed = interpolate(triggerValue);
        double angularSpeed = angularInterpolate(triggerValue);

        Logger.recordOutput("DriveCommand/trigger value calculated", triggerValue);

        double xSpeed = CONTROLLER_MODE.calculateStick(deadband(controller.getLeftY())) * speed;
        double ySpeed = CONTROLLER_MODE.calculateStick(deadband(controller.getLeftX())) * speed;
        double thetaSpeed = CONTROLLER_MODE.calculateStick(deadband(controller.getRightX())) * angularSpeed * 0.75;

        return new ChassisSpeeds(xSpeed, ySpeed, thetaSpeed);
    }
}