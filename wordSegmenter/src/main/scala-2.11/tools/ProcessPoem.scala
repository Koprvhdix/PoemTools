import scala.io.Source
import java.io.{File, PrintWriter}

/**
  * Created by wukai on 16-11-13.
  * This object is used to treat the useless text
  */
object ProcessPoem {
  def processTangPoem(): Unit = {
    val folder = "poem"

    /*
      process chapter. Tangs Poem has 900 chapters.
     */
    for (chapter <- new File(folder).listFiles()) {
      for (file <- new File(chapter.toString).listFiles()) {
        println(file)
        for (line <- Source.fromFile(file).getLines()) {
          if (!line.isEmpty) {
            val start = line.indexOf("首") + 1
            if (start != 18) {
              println("ERROR Start")
              println(line)
            } else {
              val end = line.indexOf("作者：张子蛟") - 1
              val lengthOfLine = line.length
              if (lengthOfLine - end != 39) {
                println("ERROR End")
                println(line)
              }

              /*
                get poem
               */
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
}
