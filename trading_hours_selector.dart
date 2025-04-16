import 'package:flutter/material.dart';

class TradingHoursSelector extends StatefulWidget {
  final TimeOfDay startTime;
  final TimeOfDay endTime;
  final Function(TimeOfDay, TimeOfDay) onChanged;

  const TradingHoursSelector({
    Key? key,
    required this.startTime,
    required this.endTime,
    required this.onChanged,
  }) : super(key: key);

  @override
  _TradingHoursSelectorState createState() => _TradingHoursSelectorState();
}

class _TradingHoursSelectorState extends State<TradingHoursSelector> {
  late TimeOfDay _startTime;
  late TimeOfDay _endTime;

  @override
  void initState() {
    super.initState();
    _startTime = widget.startTime;
    _endTime = widget.endTime;
  }

  String _formatTimeOfDay(TimeOfDay timeOfDay) {
    final hour = timeOfDay.hour.toString().padLeft(2, '0');
    final minute = timeOfDay.minute.toString().padLeft(2, '0');
    return '$hour:$minute';
  }

  Future<void> _selectStartTime(BuildContext context) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: _startTime,
    );
    if (picked != null && picked != _startTime) {
      setState(() {
        _startTime = picked;
      });
      widget.onChanged(_startTime, _endTime);
    }
  }

  Future<void> _selectEndTime(BuildContext context) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: _endTime,
    );
    if (picked != null && picked != _endTime) {
      setState(() {
        _endTime = picked;
      });
      widget.onChanged(_startTime, _endTime);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Horário de Operação',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _buildTimeSelector(
                    label: 'Início',
                    time: _startTime,
                    onTap: () => _selectStartTime(context),
                  ),
                ),
                SizedBox(width: 16),
                Expanded(
                  child: _buildTimeSelector(
                    label: 'Fim',
                    time: _endTime,
                    onTap: () => _selectEndTime(context),
                  ),
                ),
              ],
            ),
            SizedBox(height: 16),
            Text(
              'O robô operará apenas entre ${_formatTimeOfDay(_startTime)} e ${_formatTimeOfDay(_endTime)}.',
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTimeSelector({
    required String label,
    required TimeOfDay time,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 12, horizontal: 16),
        decoration: BoxDecoration(
          border: Border.all(color: Colors.grey[300]!),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              label,
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
            SizedBox(height: 4),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  _formatTimeOfDay(time),
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                Icon(Icons.access_time, size: 16),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
