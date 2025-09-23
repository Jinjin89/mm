import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { SafeAreaView, StyleSheet, Text, View } from 'react-native';

const modules = [
  '用户登录与权限',
  '曲库上传与转码',
  '播放记录与推荐'
];

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>音乐平台移动端</Text>
        <Text style={styles.subtitle}>Expo 驱动的开发环境已经就绪。</Text>
        {modules.map((module) => (
          <View key={module} style={styles.card}>
            <Text style={styles.cardText}>{module}</Text>
          </View>
        ))}
        <Text style={styles.note}>API: {process.env.EXPO_PUBLIC_API_URL}</Text>
      </View>
      <StatusBar style="light" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
    alignItems: 'center',
    justifyContent: 'center'
  },
  content: {
    width: '90%',
    maxWidth: 480,
    alignItems: 'center'
  },
  title: {
    fontSize: 28,
    color: '#e2e8f0',
    fontWeight: 'bold',
    marginBottom: 12
  },
  subtitle: {
    fontSize: 16,
    color: '#94a3b8',
    textAlign: 'center',
    marginBottom: 24
  },
  card: {
    width: '100%',
    padding: 16,
    borderRadius: 12,
    backgroundColor: 'rgba(30, 41, 59, 0.8)',
    marginBottom: 12,
    borderWidth: 1,
    borderColor: 'rgba(148, 163, 184, 0.3)'
  },
  cardText: {
    color: '#cbd5f5',
    fontSize: 16,
    textAlign: 'center'
  },
  note: {
    marginTop: 16,
    color: '#cbd5f5'
  }
});
