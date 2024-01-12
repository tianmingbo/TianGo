import java.lang.StringBuilder

object ArrayDemo {
  def main(args: Array[String]): Unit = {
    val arr = new Array[String](3);
    arr(0) = "1"
    arr(1) = "2"
    arr(2) = "3"
    // 遍历元素
    for (elem <- arr) {
      println(elem)
    }
    val a = StringBuilder()
    for (i <- arr.indices) {
      //根据索引遍历
      a.append(arr(i))
    }
    println(a.toString())
  }
}
