import scala.io.Source
import scala.reflect.io.Directory
import java.io.{File, PrintWriter}

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
        println(file)
        for (line <- Source.fromFile(file).getLines()) {
          if (!line.isEmpty) {
            val start = line.indexOf("首") + 1
            if (start != 18) {
              println("ERROR Start")
              println(line)
            }
            val end = line.indexOf("作者：张子蛟") - 1
            val lengOfLine = line.length
            if (lengOfLine - end != 39) {
              println("ERROR End")
              println(line)
            }
            val poemBuffer = new StringBuffer()
            for (i <- start to end) {
              poemBuffer.append(line(i).toString)
            }

            val outputFile = new PrintWriter(file)
            outputFile.println(poemBuffer.toString)
            outputFile.close()
          }
        }
      }
    }
  }
}
