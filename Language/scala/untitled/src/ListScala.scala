ArrayDemo$import java.util

object ListScala {
  def main(args: Array[String]): Unit = {
    val a = new util.ArrayList[Int](2)
    a.add(1)
    a.add(2)
    val b = List(1, 2)
    println(a)
    b.::(3)
    println(b)
  }

}
