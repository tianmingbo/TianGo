
def time(): Long = {
  println("in time")
  System.currentTimeMillis()
}

def delayed(t: => Long): Long = {
  printf("in delayed")
  println(t)
  t
}

@main def main(): Unit = {
  val a: Long = delayed(time())
  println(s"res is ${a.toString}")
}