//抽象类
abstract class AbsIterator {
  type T

  def hasNext: Boolean

  def next(): T
}

class StringIterator(s: String) extends AbsIterator {
  override type T = Char
  private var i = 0

  override def hasNext: Boolean = i < s.length

  override def next(): T = {
    val ch = s.charAt(i)
    i += 1
    ch
  }
}


trait RichIterator extends AbsIterator {
  def forEach(f: T => Unit): Unit = while (hasNext) f(next())
}

//with 混入
class RichStringIterator extends StringIterator("dali") with RichIterator

object Mixin {
  def main(args: Array[String]): Unit = {
    val obj = new RichStringIterator
    obj.forEach(println)
  }
}
