import scala.collection.mutable.ArrayBuffer

trait Iterator[A] {
  def hasNext: Boolean

  def next(): A
}

class IntIterator(to: Int) extends Iterator[Int] {
  private var cur = 0

  def hasNext: Boolean = cur < to

  override def next(): Int = {
    if (hasNext) {
      val t = cur
      cur += 1
      t
    } else 0
  }
}

object Main {
  def main(args: Array[String]): Unit = {
    val a: String = "tian"
    val b: Int = a indexOf "a"
    println(s"b = ${b}")
  }
}