package func

class SimpleRecord(a: Int
                   , b: String)


object Demo {
  def main(args: Array[String]): Unit = {
    val a = List("a", "b", "c")
    a.map{ s => new SimpleRecord(1, s) }
    a.map(new SimpleRecord(1, _)).map(_.*)
    println(a)
  }
}
