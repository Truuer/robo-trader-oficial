import 'package:flutter/material.dart';

class AssetSelectionList extends StatefulWidget {
  final List<String> selectedAssets;
  final Function(List<String>) onChanged;

  const AssetSelectionList({
    Key? key,
    required this.selectedAssets,
    required this.onChanged,
  }) : super(key: key);

  @override
  _AssetSelectionListState createState() => _AssetSelectionListState();
}

class _AssetSelectionListState extends State<AssetSelectionList> {
  final List<String> availableAssets = [
    'PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'MGLU3', 'WEGE3', 'ABEV3', 
    'BBAS3', 'ITSA4', 'B3SA3', 'RENT3', 'EGIE3', 'RADL3', 'JBSS3'
  ];
  
  final TextEditingController _searchController = TextEditingController();
  List<String> _filteredAssets = [];
  
  @override
  void initState() {
    super.initState();
    _filteredAssets = availableAssets;
    
    _searchController.addListener(() {
      _filterAssets();
    });
  }
  
  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
  
  void _filterAssets() {
    final query = _searchController.text.toLowerCase();
    setState(() {
      if (query.isEmpty) {
        _filteredAssets = availableAssets;
      } else {
        _filteredAssets = availableAssets
            .where((asset) => asset.toLowerCase().contains(query))
            .toList();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Buscar ativo...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
            SizedBox(height: 16),
            Text(
              'Ativos Selecionados: ${widget.selectedAssets.length}',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Container(
              height: 200,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey[300]!),
                borderRadius: BorderRadius.circular(8),
              ),
              child: ListView.builder(
                itemCount: _filteredAssets.length,
                itemBuilder: (context, index) {
                  final asset = _filteredAssets[index];
                  final isSelected = widget.selectedAssets.contains(asset);
                  
                  return CheckboxListTile(
                    title: Text(asset),
                    value: isSelected,
                    onChanged: (selected) {
                      List<String> newSelection = List.from(widget.selectedAssets);
                      if (selected == true) {
                        if (!newSelection.contains(asset)) {
                          newSelection.add(asset);
                        }
                      } else {
                        newSelection.remove(asset);
                      }
                      widget.onChanged(newSelection);
                    },
                    dense: true,
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
