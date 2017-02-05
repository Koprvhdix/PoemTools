package tools

import java.util.Properties

import edu.stanford.nlp.ie.crf.CRFClassifier
import edu.stanford.nlp.io.IOUtils
import edu.stanford.nlp.ling.CoreLabel

/**
  * Created by wukai on 17-2-5.
  */
class StanfordSegmenter {
  def stanfordSeg(poem: String): Unit = {
    val basedir = System.getProperty("SegDemo", "data")

    val props = new Properties()
    props.setProperty("sighanCorporaDict", basedir)
    props.setProperty("serDictionary", "data/dict-chris6.ser.gz")
    props.setProperty("inputEncoding", "UTF-8")
    props.setProperty("sighanPostProcessing", "true")

    val segmenter = new CRFClassifier[CoreLabel](props)
    segmenter.loadClassifierNoExceptions("data/ctb.gz", props)

    val segmented = segmenter.segmentString(poem)
    println(segmented)
  }
}
