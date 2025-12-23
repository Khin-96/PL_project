# Troubleshooting Guide

## Common Issues

### Data Loading Issues

**Problem: "File not found" when loading match**
- Solution: Ensure match data is in `data/raw/` directory
- Check file naming convention: `{match_id}_tracking.jsonl`

**Problem: "Invalid data format" error**
- Solution: Validate data with `DataValidator`
- Check coordinate ranges (0-105 x, 0-68 y)

**Problem: Large memory usage**
- Solution: Data is cached in NumPy format for efficiency
- Consider limiting match length or using frame range selection

### Performance Issues

**Problem: Low FPS/Stuttering**
- Solution: Reduce number of active overlays
- Toggle heatmap, pass network, or other visualizations off
- Check `PerformanceMonitor` metrics with F2

**Problem: Slow seeking/scrubbing**
- Solution: Ensure data is cached (first load may be slow)
- Increase cache size if available memory permits

### Visualization Issues

**Problem: Overlays not appearing**
- Solution: Check if overlay is enabled (toggle key)
- Verify data exists for overlay type
- Check overlay settings in config

**Problem: Sprites (players/ball) not visible**
- Solution: Verify camera is within pitch bounds
- Check sprite factory is creating sprites
- Reset view with 'X' key

### Coordinate/Position Issues

**Problem: Players appearing off-pitch**
- Solution: Check coordinate transformation in `camera_controller.py`
- Verify pitch dimensions in config
- Validate source data coordinates

**Problem: Zoom not working**
- Solution: Use Z/X keys to zoom
- Check zoom bounds in camera controller
- Try resetting view with X key

## Debug Mode

Run with debug flag to see additional information:
```bash
python src/main.py --debug
```

This enables:
- FPS and frame time display (F2)
- Verbose logging
- Performance metrics
- Development console access (F12)

## Getting Help

1. Check logs in console output
2. Review performance metrics (F2)
3. Verify data with `validate_data.py` script
4. Check troubleshooting section in README
