export interface ScalingConfig {
  minInstances: number;
  maxInstances: number;
  scalingPolicy: 'vertical' | 'horizontal' | 'hybrid';
  threshold: number;
}

export interface Metrics {
  timestamp: Date;
  latency: number;
  cost: number;
  instances: number;
}