package obj

case class Message(sender: String, receiver: String, content: List[String])

object caseClass {
  def main(args: Array[String]): Unit = {
    val msg1 = Message("Alice", "Bob", List("Hi", "Hello"))
    val msg2 = Message("Alice", "Bob", List("Hi", "Hello"))
    println(msg1 == msg2) //true样例类在比较的时候是按值比较而非按引用比较
    val msg3 = msg1.copy(receiver = "Eve")
    println(msg1)
    println(msg3)
  }
}
