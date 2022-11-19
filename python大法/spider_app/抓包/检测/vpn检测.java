try{
        Enumeration<NetworkInterface> networkInterfaces=NetworkInterface.getNetworkInterfaces();
        int count=0;
        while(networkInterfaces.hasMoreElements()){
        NetworkInterface next=networkInterfaces.nextElement();
        logOutPut("getName获得网络设备名称="+next.getName());
        logOutPut("getDisplayName获得网络设备显示名称="+next.getDisplayName());
        logOutPut("getIndex获得网络接口的索引="+next.getIndex());
        logOutPut("isUp是否已经开启并运行="+next.isUp());
        logOutPut("isBoopback是否为回调接口="+next.isLoopback());
        logOutPut("**********************"+count++);
        }
        }catch(SocketException e){
        e.printStackTrace();
        }
//getName()网卡名为tun0，next.isUp()为true说明开启了vpn

/**
 * 使用Objection把java.net下的类全hook，来查看app使用了哪些方法
 * 主要检测方法：
 * java.net.NetworkInterface.getName
 * android.net.ConnectivityManager.getNetworkCapabilities
 */