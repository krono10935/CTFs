package frc.robot.challenges;

/**
 * A room in the Easy challenge. The player must call {@link #check()} on the
 * rooms in order, starting at index 99 (the 100th room). The class watches the
 * access order and only reveals the password when the run is valid.
 */
public class Room {
  // Per-run tracker. A fresh JVM on each simulation run resets these.
  static boolean started = false;
  static boolean failed = false;
  static int trigger = -1;
  static int checkedCount = 0;

  private final int index;

  public Room(int index) {
    this.index = index;
  }

  /** Reset the shared tracker before a run and set the winning room index. */
  static void begin(int triggerIndex) {
    started = false;
    failed = false;
    trigger = triggerIndex;
    checkedCount = 0;
  }

  /** Visit this room. Prints a punishment message or the password. */
  public void check() {
    checkedCount++;
    if (failed) {
      return;
    }
    if (index < 99) {
      // Checked a room before the 100th slot.
      failed = true;
      System.out.println("You need to start from the 100th slot");
      return;
    }
    if (!started) {
      if (index == 99) {
        started = true;
      } else {
        // First room checked was past the 100th slot.
        failed = true;
        System.out.println("You must start exactly from the 100th slot");
        return;
      }
    }
    if (started && !failed && index == trigger) {
      System.out.println("The library is open");
    }
  }
}
