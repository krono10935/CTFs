package frc.robot;
import edu.wpi.first.apriltag.AprilTagFieldLayout;
import edu.wpi.first.apriltag.AprilTagFields;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.math.geometry.Translation2d;
import edu.wpi.first.math.geometry.Translation3d;
import edu.wpi.first.math.util.Units;
import frc.robot.FieldConstants.LeftTrench.LinesVertical;
import frc.utils.AllianceFlipUtil;

public class FieldConstants {
    public static final double fieldLength = AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getFieldLength();
    public static final double fieldWidth = AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getFieldWidth();

    // public static final double ALLIANCE_ZONE_X = Hub.topCenterPoint.getX(); 
     public static class Hub {

    // Dimensions
    public static final double width = Units.inchesToMeters(47.0);
    public static final double height =
        Units.inchesToMeters(72.0); // includes the catcher at the top
    public static final double innerWidth = Units.inchesToMeters(41.7);
    public static final double innerHeight = Units.inchesToMeters(56.5);

    // Relevant reference points on alliance side
    public static final Translation3d topCenterPoint =
        new Translation3d(
            AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(26).get().getX() + width / 2.0,
            fieldWidth / 2.0,
            height);
    public static final Translation3d innerCenterPoint =
        new Translation3d(
            AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(26).get().getX() + width / 2.0,
            fieldWidth / 2.0,
            innerHeight);

    public static final Translation2d nearLeftCorner =
        new Translation2d(topCenterPoint.getX() - width / 2.0, fieldWidth / 2.0 + width / 2.0);
    public static final Translation2d nearRightCorner =
        new Translation2d(topCenterPoint.getX() - width / 2.0, fieldWidth / 2.0 - width / 2.0);
    public static final Translation2d farLeftCorner =
        new Translation2d(topCenterPoint.getX() + width / 2.0, fieldWidth / 2.0 + width / 2.0);
    public static final Translation2d farRightCorner =
        new Translation2d(topCenterPoint.getX() + width / 2.0, fieldWidth / 2.0 - width / 2.0);

    // Relevant reference points on the opposite side
    public static final Translation3d oppTopCenterPoint =
        new Translation3d(
            AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(4).get().getX() + width / 2.0,
            fieldWidth / 2.0,
            height);
    public static final Translation2d oppNearLeftCorner =
        new Translation2d(oppTopCenterPoint.getX() - width / 2.0, fieldWidth / 2.0 + width / 2.0);
    public static final Translation2d oppNearRightCorner =
        new Translation2d(oppTopCenterPoint.getX() - width / 2.0, fieldWidth / 2.0 - width / 2.0);
    public static final Translation2d oppFarLeftCorner =
        new Translation2d(oppTopCenterPoint.getX() + width / 2.0, fieldWidth / 2.0 + width / 2.0);
    public static final Translation2d oppFarRightCorner =
        new Translation2d(oppTopCenterPoint.getX() + width / 2.0, fieldWidth / 2.0 - width / 2.0);

    // Hub faces
    public static final Pose2d nearFace =
        AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(26).get().toPose2d();
    public static final Pose2d farFace =
        AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(20).get().toPose2d();
    public static final Pose2d rightFace =
        AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(18).get().toPose2d();
    public static final Pose2d leftFace =
        AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(21).get().toPose2d();
  }
    public static class LeftTrench {
    // Dimensions
    public static final double width = Units.inchesToMeters(65.65);
    public static final double depth = Units.inchesToMeters(47.0);
    public static final double height = Units.inchesToMeters(40.25);
    public static final double openingWidth = Units.inchesToMeters(50.34);
    public static final double openingHeight = Units.inchesToMeters(22.25);

    public static class LinesVertical {
    public static final double center = fieldLength / 2.0;
    public static final double starting =
        AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(26).get().getX();
    public static final double allianceZone = starting;
    public static final double hubCenter =
        AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(26).get().getX() + Hub.width / 2.0;
    public static final double neutralZoneNear = center - Units.inchesToMeters(120);
    public static final double neutralZoneFar = center + Units.inchesToMeters(120);
    public static final double oppHubCenter =
        AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(4).get().getX() + Hub.width / 2.0;
    public static final double oppAllianceZone =
        AprilTagFieldLayout.loadField(AprilTagFields.k2026RebuiltWelded).getTagPose(10).get().getX();
  }

    // Relevant reference points on alliance side
    public static final Translation3d openingTopLeft =
        new Translation3d(LinesVertical.hubCenter, fieldWidth, openingHeight);
    public static final Translation3d openingTopRight =
        new Translation3d(LinesVertical.hubCenter, fieldWidth - openingWidth, openingHeight);
    public static final Translation3d openingTopCenter = 
        new Translation3d(LinesVertical.hubCenter, fieldWidth - openingWidth / 2, openingHeight);

    // Relevant reference points on opposing side
    public static final Translation3d oppOpeningTopLeft =
        new Translation3d(LinesVertical.oppHubCenter, fieldWidth, openingHeight);
    public static final Translation3d oppOpeningTopRight =
        new Translation3d(LinesVertical.oppHubCenter, fieldWidth - openingWidth, openingHeight);

    public static final Translation3d oppOpeningTopCenter = 
        new Translation3d(LinesVertical.hubCenter, fieldWidth - openingWidth / 2, openingHeight);
  }

  public static class RightTrench {

    // Dimensions
    public static final double width = Units.inchesToMeters(65.65);
    public static final double depth = Units.inchesToMeters(47.0);
    public static final double height = Units.inchesToMeters(40.25);
    public static final double openingWidth = Units.inchesToMeters(50.34);
    public static final double openingHeight = Units.inchesToMeters(22.25);

    

    // Relevant reference points on alliance side
    public static final Translation3d openingTopLeft =
        new Translation3d(LinesVertical.hubCenter, openingWidth, openingHeight);
    public static final Translation3d openingTopRight =
        new Translation3d(LinesVertical.hubCenter, 0, openingHeight);

    public static final Translation3d openingTopCenter = 
        new Translation3d(LinesVertical.hubCenter, openingWidth / 2, openingHeight);

    // Relevant reference points on opposing side
    public static final Translation3d oppOpeningTopLeft =
        new Translation3d(LinesVertical.oppHubCenter, openingWidth, openingHeight);
    public static final Translation3d oppOpeningTopRight =
        new Translation3d(LinesVertical.oppHubCenter, 0, openingHeight);

    public static final Translation3d oppOpeningTopCenter = 
        new Translation3d(LinesVertical.hubCenter, openingWidth / 2, openingHeight);
  }

    /** Left Bump related constants */
    public static class LeftBump {

        // Dimensions
        public static final double width = Units.inchesToMeters(73.0);
        public static final double height = Units.inchesToMeters(6.513);
        public static final double depth = Units.inchesToMeters(44.4);

        // Relevant reference points on alliance side
        public static final Translation2d nearLeftCorner =
                Hub.nearLeftCorner.plus(new Translation2d(0.0, width));
        public static final Translation2d nearRightCorner = Hub.nearLeftCorner;

        public static final Translation2d center = Hub.nearLeftCorner
            .plus(new Translation2d(depth / 2, width / 2));

        public static final Translation2d farLeftCorner =
                Hub.farLeftCorner.plus(new Translation2d(0.0, width));
        public static final Translation2d farRightCorner = Hub.farLeftCorner;

    }

    /** Right Bump related constants */
    public static class RightBump {
        // Dimensions
        public static final double width = Units.inchesToMeters(73.0);
        public static final double height = Units.inchesToMeters(6.513);
        public static final double depth = Units.inchesToMeters(44.4);

        // Relevant reference points on alliance side
        public static final Translation2d nearLeftCorner = Hub.nearRightCorner;
        public static final Translation2d nearRightCorner =
                Hub.nearRightCorner.minus(new Translation2d(0.0, width));

        public static final Translation2d center = Hub.farRightCorner
            .minus(new Translation2d(depth / 2, width / 2));

        public static final Translation2d farLeftCorner = Hub.farRightCorner;
        public static final Translation2d farRightCorner =
                Hub.farRightCorner.minus(new Translation2d(0.0, width));
    }


    public static Translation2d towerLeft = new Translation2d(5,5);
    public static Translation2d towerLeftBack = new Translation2d(4,4);

    public static Translation2d towerRight = new Translation2d(4,3);
    public static Translation2d towerRightBack = new Translation2d(3,4);

    public  enum TowerSide {
        LEFT,
        RIGHT,
    }

    public static Pose2d getTowerSideTargetPose(TowerSide tower, boolean driveBack) {
        if(driveBack) {
            return switch (tower) {
                case LEFT->new Pose2d(towerLeftBack.getX(),towerLeftBack.getY(), Rotation2d.fromDegrees(0));
                case RIGHT->new Pose2d(towerRightBack.getX(),towerRightBack.getY(), Rotation2d.fromDegrees(180));
            };
        }else  {
            return switch (tower) {
                case LEFT->new Pose2d(towerLeft.getX(),towerLeft.getY(), Rotation2d.fromDegrees(0));
                case RIGHT->new Pose2d(towerRight.getX(),towerRight.getY(), Rotation2d.fromDegrees(180));
            };
        }

    }

    public static boolean isInAllianceZone(Pose2d pose){
        var hubAlliance = FieldConstants.Hub.topCenterPoint;

        return AllianceFlipUtil.apply(pose).getX() <= hubAlliance.getX() && AllianceFlipUtil.apply(pose).getX() > 0;
    }



    public static Translation2d getClosestBump(Pose2d robotPose){

        if (AllianceFlipUtil.apply(robotPose).getY() < fieldWidth / 2){
            return AllianceFlipUtil.apply(RightBump.center);
        } else {
            return AllianceFlipUtil.apply(LeftBump.center);
        }
    }


}

