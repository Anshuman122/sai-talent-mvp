import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class ChartWidget extends StatefulWidget {
  final List<Map<String, dynamic>> data;

  const ChartWidget({
    super.key,
    required this.data,
  });

  @override
  State<ChartWidget> createState() => _ChartWidgetState();
}

class _ChartWidgetState extends State<ChartWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );
    _animation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    );
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      child: Column(
        children: [
          // Horizontal line chart with gradient
          Expanded(
            child: AnimatedBuilder(
              animation: _animation,
              builder: (context, child) {
                return CustomPaint(
                  painter: HorizontalLineChartPainter(
                    widget.data,
                    animationValue: _animation.value,
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 16),
          // Legend
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: widget.data.map((point) {
              return Column(
                children: [
                  Text(
                    point['date'],
                    style: GoogleFonts.poppins(
                      fontSize: 12,
                      color: const Color(0xFF6B7280),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${point['score']}%',
                    style: GoogleFonts.poppins(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: const Color(0xFF2563EB),
                    ),
                  ),
                ],
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}

class HorizontalLineChartPainter extends CustomPainter {
  final List<Map<String, dynamic>> data;
  final double animationValue;

  HorizontalLineChartPainter(this.data, {required this.animationValue});

  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;

    // Create gradient for the line
    final lineGradient = LinearGradient(
      colors: [
        const Color(0xFF2563EB),
        const Color(0xFF3B82F6),
        const Color(0xFF60A5FA),
      ],
      stops: const [0.0, 0.5, 1.0],
    );

    // Create gradient for the fill area
    final fillGradient = LinearGradient(
      begin: Alignment.topCenter,
      end: Alignment.bottomCenter,
      colors: [
        const Color(0xFF2563EB).withOpacity(0.3),
        const Color(0xFF2563EB).withOpacity(0.1),
        const Color(0xFF2563EB).withOpacity(0.05),
      ],
      stops: const [0.0, 0.5, 1.0],
    );

    final maxScore =
        data.map((e) => e['score'] as int).reduce((a, b) => a > b ? a : b);
    final minScore =
        data.map((e) => e['score'] as int).reduce((a, b) => a < b ? a : b);
    final scoreRange = maxScore - minScore;

    // Calculate points for horizontal line chart
    List<Offset> points = [];
    for (int i = 0; i < data.length; i++) {
      final x = 20 + (size.width - 40) * (i / (data.length - 1));
      final normalizedScore =
          scoreRange > 0 ? (data[i]['score'] - minScore) / scoreRange : 0.5;
      final y = 20 + (size.height - 40) * (1 - normalizedScore);
      points.add(Offset(x, y));
    }

    // Animate the path - draw line progressively from left to right
    final animatedPoints = <Offset>[];
    final totalPoints = points.length;
    final animatedCount = (totalPoints * animationValue).ceil();

    for (int i = 0; i < animatedCount && i < totalPoints; i++) {
      animatedPoints.add(points[i]);
    }

    if (animatedPoints.length < 2) return;

    // Create path for the line
    final path = Path();
    path.moveTo(animatedPoints[0].dx, animatedPoints[0].dy);
    for (int i = 1; i < animatedPoints.length; i++) {
      path.lineTo(animatedPoints[i].dx, animatedPoints[i].dy);
    }

    // Create path for the fill area
    final fillPath = Path();
    fillPath.moveTo(animatedPoints[0].dx, size.height - 20);
    fillPath.lineTo(animatedPoints[0].dx, animatedPoints[0].dy);
    for (int i = 1; i < animatedPoints.length; i++) {
      fillPath.lineTo(animatedPoints[i].dx, animatedPoints[i].dy);
    }
    fillPath.lineTo(animatedPoints.last.dx, size.height - 20);
    fillPath.close();

    // Draw gradient fill
    final fillRect = Rect.fromLTWH(0, 0, size.width, size.height);
    final fillShader = fillGradient.createShader(fillRect);
    final fillPaint = Paint()
      ..shader = fillShader
      ..style = PaintingStyle.fill;

    canvas.drawPath(fillPath, fillPaint);

    // Draw gradient line
    final lineRect = Rect.fromLTWH(0, 0, size.width, size.height);
    final lineShader = lineGradient.createShader(lineRect);
    final linePaint = Paint()
      ..shader = lineShader
      ..strokeWidth = 3
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;

    canvas.drawPath(path, linePaint);

    // Draw animated data points
    final pointPaint = Paint()
      ..color = const Color(0xFF2563EB)
      ..style = PaintingStyle.fill;

    final pointBorderPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    for (int i = 0; i < animatedPoints.length; i++) {
      final point = animatedPoints[i];
      final pointSize = 6.0;

      // Draw point border
      canvas.drawCircle(point, pointSize + 2, pointBorderPaint);
      // Draw point
      canvas.drawCircle(point, pointSize, pointPaint);
    }

    // Draw grid lines
    final gridPaint = Paint()
      ..color = const Color(0xFFE5E7EB)
      ..strokeWidth = 0.5;

    // Horizontal grid lines
    for (int i = 0; i <= 4; i++) {
      final y = 20 + (size.height - 40) * (i / 4);
      canvas.drawLine(
        Offset(20, y),
        Offset(size.width - 20, y),
        gridPaint,
      );
    }

    // Vertical grid lines
    for (int i = 0; i < data.length; i++) {
      final x = 20 + (size.width - 40) * (i / (data.length - 1));
      canvas.drawLine(
        Offset(x, 20),
        Offset(x, size.height - 20),
        gridPaint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
