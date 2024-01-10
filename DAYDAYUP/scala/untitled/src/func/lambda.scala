//匿名函数
object lambda {
  def main(args: Array[String]): Unit = {
    val a = (x: Int, y: String) => x + y.toInt
    val res = a(1, "2")
    println(res)
  }
}
