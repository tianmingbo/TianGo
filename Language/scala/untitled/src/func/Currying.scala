//函数柯里化
object Currying {
  //三个函数功能一样
  private def add(x: Int, y: Int) = x + y

  private def add1(x: Int) = (y: Int) => {
    println(x)
    x + y
  }

  private def add2(x: Int)(y: Int) = x + y


  def main(args: Array[String]): Unit = {
    println(add(1, 2))
    println(add1(1)(2))
    println(add2(1)(2))
  }

}
