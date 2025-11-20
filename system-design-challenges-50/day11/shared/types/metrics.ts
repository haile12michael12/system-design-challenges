import { Metrics } from './scaling';

export interface SimulationResult {
  simulationId: string;
  startTime: Date;
  endTime: Date;
  metrics: Metrics[];
  scalingDecisions: ScalingDecision[];
}

export interface ScalingDecision {
  timestamp: Date;
  action: 'scale_up' | 'scale_down' | 'scale_out' | 'scale_in' | 'no_action';
  reason: string;
  currentInstances: number;
  newInstances: number;
}