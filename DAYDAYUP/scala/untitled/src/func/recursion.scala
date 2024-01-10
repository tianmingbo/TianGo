//递归

object recursion {
  private def fib(n: Int): BigInt = {
    if (n <= 1)
      1
    else
      n * fib(n - 1)

  }

  def main(args: Array[String]): Unit = {
    val res = fib(100)
    println(res)
  }
}
