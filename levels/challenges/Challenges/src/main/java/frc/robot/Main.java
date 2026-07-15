// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot;

import edu.wpi.first.wpilibj.RobotBase;
import frc.robot.challenges.EasyChallenge;
import frc.robot.challenges.MediumChallenge;

public final class Main {
  private Main() {}

  public static void main(String... args) {
    // Routed by the shared progress token. Non-Hard phases run as plain Java in
    // simulation (they return before any RobotBase.startRobot); only Hard boots
    // the real robot.
    String phase = Progress.current();
    switch (phase) {
      case "HARD" -> RobotBase.startRobot(Robot::new);
      case "EASY" -> EasyChallenge.run();
      case "MEDIUM" -> MediumChallenge.run();
      default -> System.out.println(
          "No robot challenge active yet (phase: " + phase + ").");
    }
  }
}
