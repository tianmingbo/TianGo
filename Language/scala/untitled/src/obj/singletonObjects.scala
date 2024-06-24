package obj

import scala.math._

object Logger:
  def logger(msg: String): Unit = println(s"Info: $msg")

class Project(name: String):
  def _name: String = name

//伴生类
case class Circle(radius: Double) {

  import Circle._

  def area: Double = calculateArea(radius)
}

//伴生对象
object Circle {
  private def calculateArea(radius: Double): Double = Pi * pow(radius, 2.0)
}

object singletonObjects {
  def main(args: Array[String]): Unit = {
    val prj = Project("scala")
    println(prj._name)
    Logger.logger(prj._name)
    ///////////伴生对象和伴生类,类和它的伴生对象可以互相访问其私有成员
    val circle1 = Circle(5.0)
    println(circle1.area)
  }
}
