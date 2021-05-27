export interface AppConfig {
  API_URL: string;
}

const appConfig: AppConfig = {
  API_URL: process.env.API_URL || '',
};

export default appConfig;
