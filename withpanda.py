import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('default')
sns.set_palette("husl")

class DatasetAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.report_data = {}
        self.load_data()
    
    def load_data(self):
        """Load dataset with encoding detection"""
        print(f"📁 Loading dataset: {self.filepath}")
        
        try:
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    self.df = pd.read_csv(self.filepath, encoding=encoding)
                    print(f"✅ Successfully loaded with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("Could not decode file with any common encoding")
                
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return
        
        # Convert appropriate columns to numeric
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                numeric_series = pd.to_numeric(self.df[col], errors='coerce')
                if numeric_series.notna().sum() / len(self.df) > 0.8:
                    self.df[col] = numeric_series
        
        print(f"📊 Dataset shape: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns")
    
    def analyze_overall_stats(self):
        """Analyze overall dataset statistics"""
        print("🔍 Analyzing overall statistics...")
        
        # Basic info
        basic_info = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'dtypes': self.df.dtypes.value_counts().to_dict()
        }
        
        # Numeric columns analysis
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        numeric_stats = None
        if len(numeric_cols) > 0:
            numeric_stats = self.df[numeric_cols].describe()
            numeric_stats.loc['mode'] = self.df[numeric_cols].mode().iloc[0] if not self.df[numeric_cols].empty else np.nan
            numeric_stats.loc['skew'] = self.df[numeric_cols].skew()
            numeric_stats.loc['kurtosis'] = self.df[numeric_cols].kurtosis()
        
        # Categorical columns analysis
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        categorical_stats = {}
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                categorical_stats[col] = {
                    'unique_count': self.df[col].nunique(),
                    'most_frequent': self.df[col].value_counts().index[0] if not self.df[col].empty else 'N/A',
                    'most_frequent_count': self.df[col].value_counts().iloc[0] if not self.df[col].empty else 0,
                    'top_values': self.df[col].value_counts().head(10).to_dict()
                }
        
        # Missing data analysis
        missing_data = self.df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        # Correlation matrix
        correlation_matrix = None
        if len(numeric_cols) > 1:
            correlation_matrix = self.df[numeric_cols].corr()
        
        self.report_data['overall'] = {
            'basic_info': basic_info,
            'numeric_stats': numeric_stats,
            'categorical_stats': categorical_stats,
            'missing_data': missing_data,
            'correlation_matrix': correlation_matrix,
            'numeric_columns': numeric_cols.tolist(),
            'categorical_columns': categorical_cols.tolist()
        }
    
    def analyze_grouped_data(self, group_cols, analysis_name):
        """Analyze data grouped by specified columns"""
        print(f"🔗 Analyzing groups by: {' + '.join(group_cols)}")
        
        if not all(col in self.df.columns for col in group_cols):
            missing_cols = [col for col in group_cols if col not in self.df.columns]
            print(f"⚠️  Missing columns for {analysis_name}: {missing_cols}")
            return
        
        grouped = self.df.groupby(group_cols)
        
        # Group size statistics
        group_sizes = grouped.size()
        
        # Sample groups for detailed analysis (analyze all, not just sample)
        group_stats = {}
        
        # Get statistics for each group
        print(f"   Processing {grouped.ngroups:,} groups...")
        
        # For large number of groups, we'll summarize the group statistics
        if grouped.ngroups > 100:
            # Aggregate statistics across all groups
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                group_numeric_stats = grouped[numeric_cols].agg(['count', 'mean', 'std', 'min', 'max'])
            
            categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
            group_categorical_stats = {}
            if len(categorical_cols) > 0:
                for col in categorical_cols:
                    group_categorical_stats[col] = grouped[col].agg(['count', 'nunique'])
        else:
            # Detailed analysis for smaller number of groups
            group_numeric_stats = None
            group_categorical_stats = {}
            
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                group_numeric_stats = grouped[numeric_cols].describe()
        
        self.report_data[analysis_name] = {
            'group_count': grouped.ngroups,
            'group_sizes': group_sizes,
            'group_size_stats': {
                'mean': group_sizes.mean(),
                'median': group_sizes.median(),
                'min': group_sizes.min(),
                'max': group_sizes.max(),
                'std': group_sizes.std()
            },
            'largest_groups': group_sizes.nlargest(20).to_dict(),
            'group_numeric_stats': group_numeric_stats,
            'group_categorical_stats': group_categorical_stats
        }
    
    def run_full_analysis(self):
        """Run complete analysis of the dataset"""
        if self.df is None:
            print("❌ No data loaded")
            return
        
        # Overall analysis
        self.analyze_overall_stats()
        
        # Group analyses
        if 'page_id' in self.df.columns:
            self.analyze_grouped_data(['page_id'], 'page_id_groups')
        
        if all(col in self.df.columns for col in ['page_id', 'ad_id']):
            self.analyze_grouped_data(['page_id', 'ad_id'], 'page_ad_groups')
        
        print("✅ Analysis complete!")

class PDFReportGenerator:
    def __init__(self, analyzer, output_filename):
        self.analyzer = analyzer
        self.output_filename = output_filename
        self.report_data = analyzer.report_data
        self.df = analyzer.df
    
    def create_title_page(self, pdf):
        """Create title page"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.8, 'DATASET ANALYSIS REPORT', 
                ha='center', va='center', fontsize=24, fontweight='bold')
        
        # Dataset info
        basic_info = self.report_data['overall']['basic_info']
        
        info_text = f"""
Dataset: {self.analyzer.filepath}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATASET OVERVIEW:
• Total Rows: {basic_info['total_rows']:,}
• Total Columns: {basic_info['total_columns']:,}
• Memory Usage: {basic_info['memory_usage_mb']:.2f} MB

COLUMN TYPES:
"""
        
        for dtype, count in basic_info['dtypes'].items():
            info_text += f"• {dtype}: {count} columns\n"
        
        ax.text(0.1, 0.6, info_text, ha='left', va='top', fontsize=12, 
                transform=ax.transAxes, fontfamily='monospace')
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_numeric_analysis_page(self, pdf):
        """Create numeric columns analysis page"""
        numeric_stats = self.report_data['overall']['numeric_stats']
        if numeric_stats is None:
            return
        
        # Create subplots for numeric analysis
        fig = plt.figure(figsize=(8.5, 11))
        
        # Statistics table
        ax1 = plt.subplot(3, 1, 1)
        ax1.axis('tight')
        ax1.axis('off')
        ax1.set_title('Numeric Columns - Descriptive Statistics', fontsize=14, fontweight='bold', pad=20)
        
        # Create table
        table_data = numeric_stats.round(3)
        table = ax1.table(cellText=table_data.values,
                         rowLabels=table_data.index,
                         colLabels=table_data.columns,
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.2, 1.5)
        
        # Distribution plots
        numeric_cols = self.report_data['overall']['numeric_columns']
        if len(numeric_cols) > 0:
            n_cols = min(3, len(numeric_cols))
            for i, col in enumerate(numeric_cols[:6]):  # Show first 6 columns
                if i >= 6:
                    break
                row = (i // n_cols) + 2
                col_pos = (i % n_cols) + 1
                ax = plt.subplot(3, n_cols, (row-1)*n_cols + col_pos)
                
                self.df[col].hist(bins=30, alpha=0.7, ax=ax)
                ax.set_title(f'{col}\nDistribution', fontsize=10)
                ax.tick_params(labelsize=8)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_categorical_analysis_page(self, pdf):
        """Create categorical columns analysis page"""
        categorical_stats = self.report_data['overall']['categorical_stats']
        if not categorical_stats:
            return
        
        # Create summary table
        fig, axes = plt.subplots(2, 2, figsize=(8.5, 11))
        fig.suptitle('Categorical Columns Analysis', fontsize=16, fontweight='bold')
        
        # Summary statistics table
        ax1 = axes[0, 0]
        ax1.axis('tight')
        ax1.axis('off')
        ax1.set_title('Summary Statistics', fontweight='bold')
        
        summary_data = []
        for col, stats in categorical_stats.items():
            summary_data.append([
                col,
                stats['unique_count'],
                stats['most_frequent'][:20] + '...' if len(str(stats['most_frequent'])) > 20 else stats['most_frequent'],
                stats['most_frequent_count']
            ])
        
        table = ax1.table(cellText=summary_data,
                         colLabels=['Column', 'Unique Count', 'Most Frequent', 'Count'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.2, 1.5)
        
        # Bar charts for top categories
        categorical_cols = list(categorical_stats.keys())[:3]  # Show first 3
        for i, col in enumerate(categorical_cols):
            if i >= 3:
                break
            
            ax = axes[(i+1)//2, (i+1)%2] if i < 2 else axes[1, i-1]
            
            top_values = categorical_stats[col]['top_values']
            if len(top_values) > 0:
                values = list(top_values.values())[:10]
                labels = [str(k)[:15] + '...' if len(str(k)) > 15 else str(k) 
                         for k in list(top_values.keys())[:10]]
                
                bars = ax.bar(range(len(values)), values)
                ax.set_title(f'{col} - Top Values', fontweight='bold')
                ax.set_xticks(range(len(labels)))
                ax.set_xticklabels(labels, rotation=45, ha='right')
                
                # Add value labels on bars
                for bar, value in zip(bars, values):
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                           str(value), ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_correlation_page(self, pdf):
        """Create correlation analysis page"""
        correlation_matrix = self.report_data['overall']['correlation_matrix']
        if correlation_matrix is None or len(correlation_matrix.columns) < 2:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 11))
        fig.suptitle('Correlation Analysis', fontsize=16, fontweight='bold')
        
        # Correlation heatmap
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   ax=ax1, square=True, fmt='.2f')
        ax1.set_title('Correlation Matrix')
        
        # High correlation pairs
        ax2.axis('off')
        ax2.set_title('High Correlation Pairs (|r| > 0.7)', fontweight='bold')
        
        high_corr_text = ""
        high_corr_pairs = []
        
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_val = correlation_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    high_corr_pairs.append((
                        correlation_matrix.columns[i],
                        correlation_matrix.columns[j],
                        corr_val
                    ))
        
        if high_corr_pairs:
            for col1, col2, corr_val in high_corr_pairs:
                high_corr_text += f"{col1} ↔ {col2}: {corr_val:.3f}\n"
        else:
            high_corr_text = "No highly correlated pairs found (|r| > 0.7)"
        
        ax2.text(0.1, 0.9, high_corr_text, transform=ax2.transAxes, 
                fontsize=12, va='top', fontfamily='monospace')
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_group_analysis_page(self, pdf, group_name, title):
        """Create group analysis page"""
        if group_name not in self.report_data:
            return
        
        group_data = self.report_data[group_name]
        
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # Group size distribution
        ax1 = plt.subplot(3, 2, 1)
        group_sizes = group_data['group_sizes']
        
        # Histogram of group sizes
        ax1.hist(group_sizes.values, bins=50, alpha=0.7, edgecolor='black')
        ax1.set_title('Group Size Distribution')
        ax1.set_xlabel('Group Size')
        ax1.set_ylabel('Frequency')
        
        # Group size statistics
        ax2 = plt.subplot(3, 2, 2)
        ax2.axis('off')
        ax2.set_title('Group Size Statistics', fontweight='bold')
        
        size_stats = group_data['group_size_stats']
        stats_text = f"""
Total Groups: {group_data['group_count']:,}

Group Size Statistics:
• Mean: {size_stats['mean']:.1f}
• Median: {size_stats['median']:.1f}
• Min: {size_stats['min']:,}
• Max: {size_stats['max']:,}
• Std Dev: {size_stats['std']:.1f}
"""
        
        ax2.text(0.1, 0.9, stats_text, transform=ax2.transAxes,
                fontsize=10, va='top', fontfamily='monospace')
        
        # Top 10 largest groups
        ax3 = plt.subplot(3, 1, 2)
        largest_groups = group_data['largest_groups']
        top_10 = dict(list(largest_groups.items())[:10])
        
        if top_10:
            labels = [str(k)[:30] + '...' if len(str(k)) > 30 else str(k) for k in top_10.keys()]
            values = list(top_10.values())
            
            bars = ax3.bar(range(len(values)), values)
            ax3.set_title('Top 10 Largest Groups')
            ax3.set_xticks(range(len(labels)))
            ax3.set_xticklabels(labels, rotation=45, ha='right')
            ax3.set_ylabel('Group Size')
            
            # Add value labels
            for bar, value in zip(bars, values):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                        f'{value:,}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def create_missing_data_page(self, pdf):
        """Create missing data analysis page"""
        missing_data = self.report_data['overall']['missing_data']
        
        if len(missing_data) == 0:
            # No missing data page
            fig, ax = plt.subplots(figsize=(8.5, 11))
            ax.axis('off')
            ax.text(0.5, 0.5, '✅ NO MISSING DATA FOUND\n\nAll columns have complete data!',
                   ha='center', va='center', fontsize=20, fontweight='bold',
                   transform=ax.transAxes)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 11))
        fig.suptitle('Missing Data Analysis', fontsize=16, fontweight='bold')
        
        # Missing data bar chart
        missing_counts = missing_data.values
        missing_cols = [col[:20] + '...' if len(col) > 20 else col for col in missing_data.index]
        
        bars = ax1.bar(range(len(missing_counts)), missing_counts)
        ax1.set_title('Missing Data by Column')
        ax1.set_xticks(range(len(missing_cols)))
        ax1.set_xticklabels(missing_cols, rotation=45, ha='right')
        ax1.set_ylabel('Missing Count')
        
        # Add percentage labels
        total_rows = len(self.df)
        for bar, count in zip(bars, missing_counts):
            percentage = (count / total_rows) * 100
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(missing_counts)*0.01,
                    f'{percentage:.1f}%', ha='center', va='bottom', fontsize=8)
        
        # Missing data table
        ax2.axis('tight')
        ax2.axis('off')
        ax2.set_title('Missing Data Summary', fontweight='bold')
        
        table_data = []
        for col, count in missing_data.items():
            percentage = (count / total_rows) * 100
            table_data.append([col, f'{count:,}', f'{percentage:.2f}%'])
        
        table = ax2.table(cellText=table_data,
                         colLabels=['Column', 'Missing Count', 'Percentage'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.5)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def generate_report(self):
        """Generate complete PDF report"""
        print(f"📄 Generating PDF report: {self.output_filename}")
        
        with PdfPages(self.output_filename) as pdf:
            # Title page
            self.create_title_page(pdf)
            
            # Missing data analysis
            self.create_missing_data_page(pdf)
            
            # Numeric analysis
            self.create_numeric_analysis_page(pdf)
            
            # Categorical analysis
            self.create_categorical_analysis_page(pdf)
            
            # Correlation analysis
            self.create_correlation_page(pdf)
            
            # Group analyses
            if 'page_id_groups' in self.report_data:
                self.create_group_analysis_page(pdf, 'page_id_groups', 'Analysis by Page ID')
            
            if 'page_ad_groups' in self.report_data:
                self.create_group_analysis_page(pdf, 'page_ad_groups', 'Analysis by Page ID + Ad ID')
        
        print(f"✅ PDF report generated successfully: {self.output_filename}")
        print(f"📖 Open the file to view your comprehensive dataset analysis!")

def main():
    """Main function to run complete analysis and generate PDF report"""
    filepath = "2024_fb_ads_president_scored_anon.csv"  # Change as needed
    output_pdf = f"dataset_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    print("🚀 COMPREHENSIVE DATASET ANALYSIS WITH PDF REPORT")
    print("=" * 60)
    
    # Step 1: Analyze the dataset
    analyzer = DatasetAnalyzer(filepath)
    if analyzer.df is None:
        return
    
    # Step 2: Run full analysis
    analyzer.run_full_analysis()
    
    # Step 3: Generate PDF report
    report_generator = PDFReportGenerator(analyzer, output_pdf)
    report_generator.generate_report()
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print(f"📊 Analyzed {len(analyzer.df):,} rows and {len(analyzer.df.columns)} columns")
    print(f"📄 Report saved as: {output_pdf}")

if __name__ == "__main__":
    main()