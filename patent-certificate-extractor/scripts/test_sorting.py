#!/usr/bin/env python3
"""
Test script to verify sorting and grouping functionality
"""

import sys
import json
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Import functions by reading and executing the generate_excel file
import importlib.util
spec = importlib.util.spec_from_file_location("generate_excel", script_dir / "generate_excel.py")
generate_excel_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_excel_module)

sort_patent_data = generate_excel_module.sort_patent_data
normalize_patent_type = generate_excel_module.normalize_patent_type
get_patent_type_priority = generate_excel_module.get_patent_type_priority
parse_application_date = generate_excel_module.parse_application_date


def test_sorting():
    """Test the sorting logic with sample data"""
    print("Testing Patent Data Sorting")
    print("=" * 80)

    # Sample data with multiple holders and patent types
    test_data = [
        {
            '专利号': 'ZL202020217799.0',
            '专利名称': '一种新型冠状病毒抗原检测试剂盒',
            '权利人': '深圳普瑞金生物药业有限公司',
            '专利类型': '实用新型专利',
            '发明人': '包朝乐萌;吴显辉',
            '申请日期': '2020-02-26'
        },
        {
            '专利号': 'AU2019325036',
            '专利名称': 'BCMA chimeric antigen receptor based on single domain antibody',
            '权利人': 'Shenzhen Pregene Biopharma Co. Ltd.',
            '专利类型': 'Standard Patent (Invention)',
            '发明人': 'ZHANG, Jishuai; LI, Hongjian',
            '申请日期': '2019-07-10'
        },
        {
            '专利号': 'ZL201910297462.7',
            '专利名称': 'CD22单域抗体、核苷酸序列及试剂盒',
            '权利人': '深圳普瑞金生物药业有限公司',
            '专利类型': '发明专利',
            '发明人': '李胜华;包朝乐戎',
            '申请日期': '2019-04-12'
        },
        {
            '专利号': 'ZL2019102974612',
            '专利名称': 'VEGF单域抗体、核苷酸序列及试剂盒',
            '权利人': '深圳普瑞金生物药业有限公司',
            '专利类型': '发明专利',
            '发明人': '李胜华;李莹莹',
            '申请日期': '2019-04-10'
        },
        {
            '专利号': 'ZL2020202178118',
            '专利名称': '一种新型冠状病毒IgM、IgG抗体联合检测试剂盒',
            '权利人': '深圳普瑞金生物药业有限公司',
            '专利类型': '实用新型专利',
            '发明人': '包朝乐萌;张继帅',
            '申请日期': '2020-02-27'
        },
        {
            '专利号': 'US17-270788',
            '专利名称': 'Anti-BCMA single domain antibody and its application',
            '权利人': 'Shenzhen Pregene Biopharma Co. Ltd.',
            '专利类型': 'Invention',
            '发明人': 'ZHANG, Jishuai; SU, Hongchang',
            '申请日期': '2020-06-01'
        }
    ]

    print("\n[Original Data]")
    for i, entry in enumerate(test_data, 1):
        print(f"{i}. {entry['权利人'][:30]:30} | {entry['专利类型']:20} | {entry['申请日期']} | {entry['专利号']}")

    # Sort the data
    sorted_data = sort_patent_data(test_data)

    print("\n[Sorted Data]")
    print("\nSort order:")
    print("  1. 权利人 (字母顺序)")
    print("  2. 专利类型 (发明专利 > 实用新型专利 > 外观设计专利)")
    print("  3. 申请日期 (降序，更晚的日期在前面)")
    print()

    for i, entry in enumerate(sorted_data, 1):
        holder = entry['权利人']
        patent_type = normalize_patent_type(entry['专利类型'])
        priority = get_patent_type_priority(patent_type)
        date_str = entry['申请日期']
        date_obj = parse_application_date(date_str)

        print(f"{i}. {holder[:30]:30} | {patent_type:20} | {date_str} | {entry['专利号']}")
        print(f"   Priority: {priority} | Type: {patent_type}")

        # Show grouping indicators
        if i == 1:
            print("   [新权利人组开始]")
        elif i > 1:
            prev_holder = sorted_data[i-2]['权利人']
            if holder != prev_holder:
                print("   [新权利人组开始]")
            else:
                prev_type = normalize_patent_type(sorted_data[i-2]['专利类型'])
                if patent_type != prev_type:
                    print("   [新专利类型]")

    # Test edge cases
    print("\n[Testing Edge Cases]")
    print("-" * 80)

    test_edge_cases = [
        {'专利类型': 'Invention Patent', '申请日期': '2024/12/31'},
        {'专利类型': 'Utility Model', '申请日期': '2024-01-01'},
        {'专利类型': '外观设计', '申请日期': '2023-12-31'},
        {'专利类型': 'Invention', '申请日期': '2023年01月01日'},
        {'专利类型': '', '申请日期': ''},
        {'专利类型': 'Unknown Type', '申请日期': 'Invalid Date'}
    ]

    for case in test_edge_cases:
        patent_type = case['专利类型']
        date_str = case['申请日期']
        normalized = normalize_patent_type(patent_type)
        priority = get_patent_type_priority(normalized)
        date_obj = parse_application_date(date_str)

        print(f"Type: '{patent_type}' -> Normalized: '{normalized}' -> Priority: {priority}")
        print(f"Date: '{date_str}' -> Parsed: {date_obj}")
        print()

    # Save sorted data to JSON for Excel generation
    output_file = script_dir.parent / 'test_sorted_data.json'
    output_file.write_text(json.dumps(sorted_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Sorted data saved to: {output_file}")

    return sorted_data


def main():
    """Run the test"""
    sorted_data = test_sorting()

    print("\n" + "=" * 80)
    print("Test Complete!")
    print("\nNext steps:")
    print("  1. Review the sorted output above")
    print("  2. Generate Excel file with sorted data:")
    print(f"     python generate_excel.py /tmp/test_sorted_patents.xlsx '{json.dumps(sorted_data)}'")


if __name__ == "__main__":
    main()
