import 'package:flutter/material.dart';

class AssessmentCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;
  final bool isEnabled;

  const AssessmentCard({
    super.key,
    required this.icon,
    required this.title,
    required this.description,
    this.isEnabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isEnabled
            ? const Color(0xFF1A1D29).withOpacity(0.8)
            : const Color(0xFF1A1D29).withOpacity(0.4),
        borderRadius: BorderRadius.circular(15),
        border: Border.all(
          color: isEnabled
              ? Colors.blue.withOpacity(0.3)
              : Colors.grey.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: isEnabled
                  ? Colors.blue.withOpacity(0.2)
                  : Colors.grey.withOpacity(0.2),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(
              icon,
              color: isEnabled ? Colors.blue : Colors.grey,
              size: 24,
            ),
          ),
          const SizedBox(width: 15),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: isEnabled ? Colors.white : Colors.grey,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 5),
                Text(
                  description,
                  style: TextStyle(
                    color: isEnabled ? Colors.white70 : Colors.grey,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
          if (isEnabled)
            const Icon(
              Icons.check_circle,
              color: Colors.green,
              size: 20,
            )
          else
            const Icon(
              Icons.lock,
              color: Colors.grey,
              size: 20,
            ),
        ],
      ),
    );
  }
}
