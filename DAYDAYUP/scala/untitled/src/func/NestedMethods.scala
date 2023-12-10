package func

//嵌套方法
object NestedMethods {
  def main(args: Array[String]): Unit = {
    def out(x: Int): Int = {
      val time = 40

      //有点闭包的意思
      def in(x: Int): Int = {
        x * time
      }

      in(x) + 4
    }

    println(out(5))
  }
}
