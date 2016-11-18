import scala.io.Source
import scala.reflect.io.Directory
import java.io.File

import scala.collection.mutable.ArrayBuffer

/**
  * Created by wukai on 16-11-13.
  * This object is used to treat the useless text
  */
object PretreatPoem {
  def main(args: Array[String]): Unit = {
    val folder = "poem"
    for (chapter <- new File(folder).listFiles()) {
      for (file <- new File(chapter.toString).listFiles()) {
        for (line <- Source.fromFile(file).getLines()) {
          if (!line.isEmpty) {

          }
        }
      }
    }
  }
}
