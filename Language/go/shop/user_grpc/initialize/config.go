package initialize

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/nacos-group/nacos-sdk-go/clients"
	"github.com/nacos-group/nacos-sdk-go/common/constant"
	"github.com/nacos-group/nacos-sdk-go/vo"
	"github.com/spf13/viper"
	"go.uber.org/zap"
	"lGo/shop/user_grpc/global"
	"path"
	"runtime"
)

func getAbsPath() string {
	var abPath string
	_, filename, _, ok := runtime.Caller(2)
	if ok {
		abPath = path.Dir(filename)
	}
	return abPath
}

func InitConfig() {
	viper.SetConfigName("config")
	// 配置文件类型
	viper.SetConfigType("yaml")
	// 配置文件搜索路径
	viper.AddConfigPath(getAbsPath()) // 当前目录

	// 读取配置文件
	if err := viper.ReadInConfig(); err != nil {
		var configFileNotFoundError viper.ConfigFileNotFoundError
		if errors.As(err, &configFileNotFoundError) {
			// 配置文件不存在（可选处理）
			zap.S().Infof("配置文件未找到，使用默认值或环境变量")
			return
		}
	}
	if err := viper.Unmarshal(&global.NacosConfig); err != nil {
		zap.S().Errorf("配置文件解析失败: %v", err)
		return
	}
	zap.S().Info("配置解析成功")

	//从nacos中读取配置信息
	sc := []constant.ServerConfig{
		{
			IpAddr: global.NacosConfig.Host,
			Port:   global.NacosConfig.Port,
		},
	}

	cc := constant.ClientConfig{
		NamespaceId:         global.NacosConfig.Namespace,
		TimeoutMs:           5000,
		NotLoadCacheAtStart: true,
		LogDir:              "tmp/nacos/log",
		CacheDir:            "tmp/nacos/cache",
		LogLevel:            "debug",
		Username:            global.NacosConfig.User,
		Password:            global.NacosConfig.Password,
	}

	configClient, err := clients.CreateConfigClient(map[string]interface{}{
		"serverConfigs": sc,
		"clientConfig":  cc,
	})
	if err != nil {
		zap.S().Errorf("connect nacos失败: %v", err)
		return
	}
	//获取配置
	content, err := configClient.GetConfig(vo.ConfigParam{
		DataId: global.NacosConfig.DataId,
		Group:  global.NacosConfig.Group})

	//监听配置变化
	err = configClient.ListenConfig(vo.ConfigParam{
		DataId: global.NacosConfig.DataId,
		Group:  global.NacosConfig.Group,
		OnChange: func(namespace, group, dataId, data string) {
			fmt.Println("group:" + group + ", dataId:" + dataId + ", data:" + data)
			zap.S().Info("config changed")
			err = json.Unmarshal([]byte(data), &global.Config)
			if err != nil {
				zap.S().Info("reload nacos配置失败： %s", err.Error())
			}
		},
	})

	err = json.Unmarshal([]byte(content), &global.Config)
	if err != nil {
		zap.S().Fatalf("读取nacos配置失败： %s", err.Error())
	}
	zap.S().Info("read nacos config success")
}
