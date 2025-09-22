import 'package:flutter/material.dart';

class ModelDownloadCard extends StatelessWidget {
  final String title;
  final String description;
  final bool isDownloaded;
  final bool isLoading;
  final VoidCallback onDownload;

  const ModelDownloadCard({
    super.key,
    required this.title,
    required this.description,
    required this.isDownloaded,
    required this.isLoading,
    required this.onDownload,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDownloaded
            ? const Color(0xFF1A1D29).withOpacity(0.8)
            : const Color(0xFF1A1D29).withOpacity(0.8),
        borderRadius: BorderRadius.circular(15),
        border: Border.all(
          color: isDownloaded
              ? Colors.green.withOpacity(0.3)
              : Colors.orange.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: isDownloaded
                  ? Colors.green.withOpacity(0.2)
                  : Colors.orange.withOpacity(0.2),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(
              isDownloaded ? Icons.download_done : Icons.download,
              color: isDownloaded ? Colors.green : Colors.orange,
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
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 5),
                Text(
                  description,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
          if (isLoading)
            const SizedBox(
              width: 20,
              height: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.orange),
              ),
            )
          else if (isDownloaded)
            const Icon(
              Icons.check_circle,
              color: Colors.green,
              size: 20,
            )
          else
            IconButton(
              onPressed: onDownload,
              icon: const Icon(
                Icons.download,
                color: Colors.orange,
                size: 20,
              ),
            ),
        ],
      ),
    );
  }
}
