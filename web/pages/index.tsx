import Head from 'next/head';
import styles from '../styles/Home.module.css';

const modules = [
  {
    title: '后端服务',
    description: 'Django + Celery + MinIO 构成的本地化音频处理后端。'
  },
  {
    title: 'Web 前端',
    description: 'Next.js 播放器，集成登录、搜索与推荐等功能。'
  },
  {
    title: '移动端',
    description: 'React Native (Expo) 客户端支持后台播放与离线缓存。'
  }
];

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>音乐平台任务看板</title>
        <meta name="description" content="Self-hosted 音乐平台全栈架构" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>音乐平台任务总览</h1>
        <p className={styles.subtitle}>
          使用 docker-compose 一键启动的全栈开发环境，覆盖 README 中的核心模块。
        </p>

        <div className={styles.grid}>
          {modules.map((module) => (
            <div key={module.title} className={styles.card}>
              <h2>{module.title}</h2>
              <p>{module.description}</p>
            </div>
          ))}
        </div>

        <div className={styles.note}>
          <p>
            后端 API 地址：<code>{process.env.NEXT_PUBLIC_API_URL}</code>
          </p>
        </div>
      </main>
    </div>
  );
}
