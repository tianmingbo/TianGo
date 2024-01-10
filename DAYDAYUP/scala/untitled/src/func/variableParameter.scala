//可变参数
object variableParameter {
  private def printfStrings(args: String*): Unit = {
    var i: Int = 1
    for (elem <- args) {
      println(s"arg[$i] is ${elem}")
      i += 1
    }
  }

  def main(args: Array[String]): Unit = {
    printfStrings("1", "2", "3")
  }
}
