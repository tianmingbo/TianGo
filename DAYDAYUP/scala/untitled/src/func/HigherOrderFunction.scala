object HigherOrderFunction {
  // 函数 f 和 值 v 作为参数，而函数 f 又调用了参数 v
  def apply(f: String => String, v: String): String = f(v)

  private def layout[A](x: A): String = "[" + x + "]"

  def main(args: Array[String]): Unit = {
    val a: String = apply(layout, "100")
    println(a)
  }
}
