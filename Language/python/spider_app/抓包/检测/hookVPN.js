function hook_vpn() {
    Java.perform(function () {
        var NetworkInterface = Java.use("java.net.NetworkInterface");
        NetworkInterface.getName.implementation = function () {
            var name = this.getName();  //hook java层的getName方法
            console.log("name: " + name);
            if (name === "tun0" || name === "ppp0") {
                return "rmnet_data0";
            } else {
                return name;
            }
        }

////////////////////////////////////////////////////////////////////////////
        var NetworkCapabilities = Java.use("android.net.NetworkCapabilities");
        NetworkCapabilities.hasTransport.implementation = function () {
            return false;
        }
/////////////////////////////////////////////////////////////////////////////
        NetworkCapabilities.appendStringRepresentationOfBitMaskToStringBuilder.implementation = function (sb, bitMask, nameFetcher, separator) {
            if (bitMask == 18) {
                console.log("bitMask", bitMask);
                sb.append("WIFI");
            } else {
                console.log(sb, bitMask);
                this.appendStringRepresentationOfBitMaskToStringBuilder(sb, bitMask, nameFetcher, separator);
            }
        }


    })
}


