// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot;

import java.util.function.BooleanSupplier;
import java.util.function.Supplier;

import org.littletonrobotics.conduit.ConduitApi;
import org.littletonrobotics.junction.AutoLog;
import org.littletonrobotics.junction.Logger;

import frc.robot.Constants;
import edu.wpi.first.math.geometry.Translation2d;
import edu.wpi.first.math.kinematics.ChassisSpeeds;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.InstantCommand;
import edu.wpi.first.wpilibj2.command.button.CommandXboxController;
import edu.wpi.first.wpilibj2.command.button.Trigger;
import frc.robot.commands.drivetrain.DriveCommand;
import frc.robot.subsystems.drivetrain.Drivetrain;
import frc.robot.subsystems.drivetrain.constants.ChassisType;

public class RobotContainer {
  private static RobotContainer instance = null;
  private final Drivetrain drivetrain;
  private final CommandXboxController controller;
  private final BooleanSupplier isAtTargetSpeed;
  private final BooleanSupplier isAtTargetPosition;
  private final Trigger atGoal;

  public static RobotContainer getInstance() {
    if (instance == null) {
        instance = new RobotContainer();
    }
    return instance;
  }

  private RobotContainer() {
    drivetrain = new Drivetrain(ConduitApi.getInstance()::getPDPVoltage, ChassisType.DEVBOT.constants);
    controller = new CommandXboxController(0);

    isAtTargetSpeed = () -> {
      ChassisSpeeds speeds = drivetrain.getChassisSpeeds();
      double magnitude = Math.hypot(speeds.vxMetersPerSecond, speeds.vyMetersPerSecond);
      return magnitude >= Constants.SPEED_THRESHOLD_MPS;
    };

    isAtTargetPosition = () -> {
      Translation2d position = drivetrain.getEstimatedPosition().getTranslation();
      Translation2d distance = Constants.GOAL.minus(position);
      double distanceMagnitude = Math.hypot(distance.getX(), distance.getY());
      Logger.recordOutput("distance", distanceMagnitude);
      return distanceMagnitude <= Constants.POSITION_TOLERANCE_METERS;
    };

    atGoal = new Trigger(isAtTargetPosition).and(new Trigger(isAtTargetSpeed));
    atGoal.onTrue(new InstantCommand(() -> drivetrain.stop()).repeatedly());
    atGoal.onTrue(new InstantCommand(() -> Logger.recordOutput("Done", true)));


    configureBindings();
  }

  private void configureBindings() {
    drivetrain.setDefaultCommand(new DriveCommand(drivetrain, controller));

    
  }

  public Command getAutonomousCommand() {
    return Commands.print("No autonomous command configured");
  }
}
