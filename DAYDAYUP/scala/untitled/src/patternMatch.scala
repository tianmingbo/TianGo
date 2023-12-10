import scala.util.Random

abstract class Notification

case class Email(sender: String, title: String, body: String) extends Notification

case class SMS(caller: String, message: String) extends Notification

case class VoiceRecording(contactName: String, link: String) extends Notification

def showNotification(notification: Notification): String = {
  notification match
    case Email(sender, title, _) =>
      s"Email from $sender with title $title"

    case SMS(caller, message) =>
      s"SMS from $caller with message $message"

    case VoiceRecording(contactName, link) =>
      s"Voice recording from $contactName with link $link"
}

object patternMatch {
  def main(args: Array[String]): Unit = {
    val x: Int = Random.nextInt(10)
    x match
      case 1 => println("one")
      case 2 => println("two")
      case 3 => println("three")
      case _ => println("other")
    //////////// case class match
    val email = Email("abc", "abc", "abc")
    println(showNotification(email))

  }
}
