import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../widgets/model_card.dart';
import '../services/model_service.dart';

class ModelsScreen extends StatefulWidget {
  const ModelsScreen({super.key});

  @override
  State<ModelsScreen> createState() => _ModelsScreenState();
}

class _ModelsScreenState extends State<ModelsScreen> {
  final ModelService _modelService = ModelService();
  bool _isLoading = false;

  // All available models data
  final List<Map<String, dynamic>> _allModels = [
    {
      'id': 'shuttle_run',
      'name': 'Shuttle Run Model',
      'description':
          'Analyzes agility and speed in shuttle run exercises with high accuracy',
      'version': 'v2.1.0',
      'size': '15.2 MB',
      'accuracy': '94.5%',
      'icon': Icons.directions_run,
      'color': const Color(0xFF3B82F6),
      'isDownloaded': false,
    },
    {
      'id': 'endurance_check',
      'name': 'Endurance Check Model',
      'description':
          'Evaluates cardiovascular endurance and stamina performance',
      'version': 'v1.8.2',
      'size': '12.7 MB',
      'accuracy': '91.3%',
      'icon': Icons.favorite,
      'color': const Color(0xFFEF4444),
      'isDownloaded': false,
    },
    {
      'id': 'situp_count',
      'name': 'Sit-up Count Model',
      'description': 'Automatically counts sit-ups and analyzes form technique',
      'version': 'v3.0.1',
      'size': '18.9 MB',
      'accuracy': '96.8%',
      'icon': Icons.fitness_center,
      'color': const Color(0xFF10B981),
      'isDownloaded': false,
    },
    {
      'id': 'pushup_analysis',
      'name': 'Push-up Analysis Model',
      'description':
          'Analyzes push-up technique and counts repetitions accurately',
      'version': 'v2.5.3',
      'size': '14.3 MB',
      'accuracy': '93.7%',
      'icon': Icons.accessibility_new,
      'color': const Color(0xFFF59E0B),
      'isDownloaded': false,
    },
    {
      'id': 'jump_assessment',
      'name': 'Jump Assessment Model',
      'description': 'Measures vertical jump height and power output',
      'version': 'v1.9.4',
      'size': '11.6 MB',
      'accuracy': '89.2%',
      'icon': Icons.trending_up,
      'color': const Color(0xFF8B5CF6),
      'isDownloaded': false,
    },
    {
      'id': 'balance_test',
      'name': 'Balance Test Model',
      'description': 'Evaluates balance and stability performance metrics',
      'version': 'v2.3.7',
      'size': '13.8 MB',
      'accuracy': '92.1%',
      'icon': Icons.balance,
      'color': const Color(0xFF06B6D4),
      'isDownloaded': false,
    },
  ];

  @override
  void initState() {
    super.initState();
    _checkDownloadedModels();
  }

  Future<void> _checkDownloadedModels() async {
    setState(() => _isLoading = true);
    try {
      for (int i = 0; i < _allModels.length; i++) {
        final isDownloaded =
            await _modelService.isModelDownloaded(_allModels[i]['id']);
        setState(() {
          _allModels[i]['isDownloaded'] = isDownloaded;
        });
      }
    } catch (e) {
      debugPrint('Error checking downloaded models: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _downloadModel(int index) async {
    setState(() => _isLoading = true);
    try {
      await _modelService.downloadModel(_allModels[index]['id']);
      setState(() {
        _allModels[index]['isDownloaded'] = true;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            '${_allModels[index]['name']} downloaded successfully!',
            style: GoogleFonts.poppins(),
          ),
          backgroundColor: const Color(0xFF10B981),
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Error downloading ${_allModels[index]['name']}: $e',
            style: GoogleFonts.poppins(),
          ),
          backgroundColor: const Color(0xFFEF4444),
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFAFAFA),
      body: SafeArea(
        child: _isLoading
            ? const Center(
                child: CircularProgressIndicator(
                  valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF2563EB)),
                ),
              )
            : CustomScrollView(
                slivers: [
                  _buildAppBar(),
                  _buildHeaderSection(),
                  _buildModelsSection(),
                  const SliverToBoxAdapter(
                    child: SizedBox(height: 40),
                  ),
                ],
              ),
      ),
    );
  }

  Widget _buildAppBar() {
    return SliverAppBar(
      expandedHeight: 100,
      floating: false,
      pinned: true,
      backgroundColor: Colors.white,
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      leading: IconButton(
        icon: const Icon(Icons.arrow_back_ios,
            color: Color(0xFF374151), size: 20),
        onPressed: () => Navigator.of(context).pop(),
      ),
      flexibleSpace: FlexibleSpaceBar(
        title: Text(
          'AI Models',
          style: GoogleFonts.poppins(
            fontWeight: FontWeight.w600,
            fontSize: 20,
            color: const Color(0xFF1F2937),
            letterSpacing: -0.5,
          ),
        ),
        centerTitle: true,
      ),
    );
  }

  Widget _buildHeaderSection() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(24, 32, 24, 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Download AI Models',
              style: GoogleFonts.poppins(
                fontSize: 28,
                fontWeight: FontWeight.w700,
                color: const Color(0xFF1F2937),
                height: 1.2,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              'Choose from our collection of advanced AI models designed for comprehensive sports talent assessment.',
              style: GoogleFonts.poppins(
                fontSize: 16,
                color: const Color(0xFF6B7280),
                height: 1.5,
              ),
            ),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFF0F9FF),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: const Color(0xFFBAE6FD),
                  width: 1,
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    Icons.info_outline,
                    color: const Color(0xFF0EA5E9),
                    size: 20,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Models are downloaded locally for offline use and better performance.',
                      style: GoogleFonts.poppins(
                        fontSize: 14,
                        color: const Color(0xFF0C4A6E),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildModelsSection() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.fromLTRB(24, 0, 24, 0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Available Models',
              style: GoogleFonts.poppins(
                fontSize: 22,
                fontWeight: FontWeight.w600,
                color: const Color(0xFF1F2937),
                letterSpacing: -0.5,
              ),
            ),
            const SizedBox(height: 24),
            ..._allModels.map((model) => Padding(
                  padding: const EdgeInsets.only(bottom: 16),
                  child: ModelCard(
                    model: model,
                    onDownload: () => _downloadModel(_allModels.indexOf(model)),
                    isLoading: _isLoading,
                  ),
                )),
          ],
        ),
      ),
    );
  }
}
