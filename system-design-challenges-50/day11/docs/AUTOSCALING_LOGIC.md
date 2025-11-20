# Autoscaling Logic

## Decision Algorithm

The autoscaling decision algorithm follows these rules:

1. **Scale Up/Out**: When workload exceeds 150% of current capacity
   - If instances ≤ 5: Scale up (vertical scaling)
   - If instances > 5: Scale out (horizontal scaling)

2. **Scale Down/In**: When workload is below 50% of current capacity
   - If instances > 1: Scale down (vertical scaling)
   - If instances = 1: Scale in (horizontal scaling)

3. **No Action**: When workload is within 50-150% of current capacity

## Capacity Calculation

Capacity is calculated as:
```
capacity = instances * 10
```

## Cost Considerations

- **Vertical Scaling**: 1.5x cost multiplier
- **Horizontal Scaling**: 1.2x cost multiplier

## Latency Considerations

- Higher instance counts generally reduce latency
- Vertical scaling can improve performance per instance