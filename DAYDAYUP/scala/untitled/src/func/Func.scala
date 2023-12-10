package func

object Func {
  def main(args: Array[String]): Unit = {
    val a = (x: Int) => x + 1
    println(a(1))
  }
}
