package config

type FileConfig struct {
	ConfigFile string
	LogFile    string
}

type Config struct {
	Server struct {
		Name   string `mapstructure:"name"`
		Env    string `mapstructure:"env"`
		Port   int    `mapstructure:"port"`
		JwtKey string `mapstructure:"jwtKey"`
	} `mapstructure:"server"`
	Database struct {
		Host     string `mapstructure:"host"`
		Port     int    `mapstructure:"port"`
		User     string `mapstructure:"user"`
		Password string `mapstructure:"password"`
		DBName   string `mapstructure:"dbname"`
	} `mapstructure:"database"`
	Logging struct {
		Level  string `mapstructure:"level"`
		Format string `mapstructure:"format"`
		Output string `mapstructure:"output"`
	} `mapstructure:"logging"`
}
