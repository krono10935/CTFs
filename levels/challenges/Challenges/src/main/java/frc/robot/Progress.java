package frc.robot;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Reads the shared progress token that the Tkinter app writes to
 * ~/.kronoctf/progress.txt, so Main knows which challenge to run.
 */
public final class Progress {
  private Progress() {}

  private static final Path PROGRESS_FILE =
      Paths.get(System.getProperty("user.home"), ".kronoctf", "progress.txt");

  /** Current phase token (LEVEL_1..HARD, DONE); LEVEL_1 if unreadable. */
  public static String current() {
    try {
      return Files.readString(PROGRESS_FILE).trim();
    } catch (IOException e) {
      return "LEVEL_1";
    }
  }
}
