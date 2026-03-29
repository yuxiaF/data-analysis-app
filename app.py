import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import os

# 自定义 CSS 样式
st.markdown("""
<style>
    /* 全局样式 */
    body {
        background-color: #f5f7f5;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #333333;
    }
    
    /* 主容器样式 */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* 侧边栏样式 */
    .sidebar {
        background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* 卡片样式 */
    .card {
        background-color: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* 按钮样式 */
    .stButton>button {
        background-color: white;
        color: #4caf50;
        border-radius: 10px;
        border: 2px solid #4caf50;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #4caf50;
        color: white;
        transform: translateY(-1px);
    }
    
    /* 标题样式 */
    .css-10trblm {
        color: #2e7d32;
        font-weight: 600;
        margin-bottom: 16px;
    }
    
    /* 标签页样式 */
    .stTabs {
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f9f0;
        border-radius: 10px;
        padding: 10px 20px;
        color: #2e7d32;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"].selected {
        background-color: #4caf50;
        color: white;
        transform: translateY(-1px);
    }
    
    /* 数据框样式 */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* 聊天消息样式 */
    .stChatMessage {
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        max-width: 80%;
    }
    
    .stChatMessage[data-role="user"] {
        background-color: #e3f2fd;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .stChatMessage[data-role="assistant"] {
        background-color: #e8f5e8;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }
    
    /* 输入框样式 */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px 16px;
        transition: all 0.2s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4caf50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
    }
    
    /* 选择框样式 */
    .stSelectbox>div>div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.2s ease;
    }
    
    .stSelectbox>div>div:hover {
        border-color: #4caf50;
    }
    
    /* 多选择框样式 */
    .stMultiSelect>div>div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.2s ease;
    }
    
    .stMultiSelect>div>div:hover {
        border-color: #4caf50;
    }
    
    /* 文件上传样式 */
    .stFileUploader>div>div {
        border-radius: 10px;
        border: 2px dashed #e0e0e0;
        transition: all 0.2s ease;
    }
    
    .stFileUploader>div>div:hover {
        border-color: #4caf50;
        background-color: #f8fff8;
    }
    
    /* 标题样式 */
    h1, h2, h3, h4, h5, h6 {
        color: #2e7d32;
        font-weight: 600;
    }
    
    /* 正文样式 */
    p {
        color: #555555;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# 设置应用标题
st.title('🌿 数据分析应用 �')

# 左侧边栏文件上传
with st.sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.header('文件上传')
    uploaded_file = st.file_uploader('上传 CSV 或 Excel 文件', type=['csv', 'xlsx', 'xls'])
    
    # 行业选择下拉框
    industry = None
    if uploaded_file is not None:
        st.header('行业选择')
        industry = st.selectbox(
            '请选择行业',
            ['零售', '制造业', '科技行业', '广告投放行业']
        )
    
    # DeepSeek API Key 配置
    st.header('API 配置')
    api_key = st.text_input('DeepSeek API Key', type='password', placeholder='输入您的 API Key 或使用环境变量')
    st.markdown('</div>', unsafe_allow_html=True)

# 数据读取和预览
if uploaded_file is not None:
    try:
        # 根据文件类型读取数据
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:  # Excel 文件
            df = pd.read_excel(uploaded_file)
        
        # 显示数据预览
        st.sidebar.subheader('数据预览')
        st.sidebar.dataframe(df.head())
        
        # 显示数据基本信息
        st.sidebar.subheader('数据信息')
        st.sidebar.write(f'行数: {df.shape[0]}')
        st.sidebar.write(f'列数: {df.shape[1]}')
        st.sidebar.write('列名:')
        st.sidebar.write(list(df.columns))
        
    except Exception as e:
        st.sidebar.error(f'读取文件时出错: {str(e)}')

# 数据清洗功能
if uploaded_file is not None:
    # 创建清洗后的数据副本
    cleaned_df = df.copy()
    
    # 1. 删除完全空的行和列
    cleaned_df = cleaned_df.dropna(how='all')
    cleaned_df = cleaned_df.dropna(axis=1, how='all')
    
    # 2. 填充缺失值
    # 对数值列填充中位数
    numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
    cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].median())
    
    # 对文本列填充"未知"
    text_cols = cleaned_df.select_dtypes(include=['object']).columns
    cleaned_df[text_cols] = cleaned_df[text_cols].fillna('未知')
    
    # 3. 去除重复行
    cleaned_df = cleaned_df.drop_duplicates()
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(['数据清洗', '可视化看板', '行业看板', '数据下载'])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # 右侧主区域显示清洗后的数据
        st.subheader('清洗后数据预览')
        st.dataframe(cleaned_df.head())
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # 显示清洗前后的对比信息
        st.subheader('数据清洗信息')
        col1, col2 = st.columns(2)
        with col1:
            st.write('清洗前:')
            st.write(f'行数: {df.shape[0]}')
            st.write(f'列数: {df.shape[1]}')
        with col2:
            st.write('清洗后:')
            st.write(f'行数: {cleaned_df.shape[0]}')
            st.write(f'列数: {cleaned_df.shape[1]}')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        # 可视化看板功能
        st.subheader('可视化看板')
        
        # 智能识别数值列和类别列
        numeric_cols = cleaned_df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = cleaned_df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # 自动检测日期列
        date_cols = []
        for col in cleaned_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['日期', '时间', 'month', 'date', 'time']):
                date_cols.append(col)
        
        # 如果有多列数值，允许用户选择
        selected_numeric_cols = []
        if numeric_cols:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('图表配置')
            selected_numeric_cols = st.multiselect(
                '请选择用于图表的数值列',
                numeric_cols,
                default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 数值列分布：直方图
        if selected_numeric_cols:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('数值列分布')
            for col in selected_numeric_cols:
                fig = px.histogram(cleaned_df, x=col, title=f'{col}分布', 
                                  color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                                  template='plotly_white')
                st.plotly_chart(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 数值列随时间趋势
        if selected_numeric_cols:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('数值列趋势')
            if date_cols:
                # 使用第一个日期列
                date_col = date_cols[0]
                for col in selected_numeric_cols:
                    fig = px.line(cleaned_df, x=date_col, y=col, title=f'{col}随{date_col}趋势',
                                 color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                                 template='plotly_white')
                st.plotly_chart(fig)
            else:
                # 用行号作为X轴
                for col in selected_numeric_cols:
                    fig = px.line(cleaned_df, x=cleaned_df.index, y=col, title=f'{col}趋势',
                                 color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                                 template='plotly_white')
                st.plotly_chart(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 类别对比
        if selected_numeric_cols and categorical_cols:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('类别对比')
            for cat_col in categorical_cols:
                # 限制类别数量，避免图表过于拥挤
                if cleaned_df[cat_col].nunique() <= 10:
                    for num_col in selected_numeric_cols:
                        fig = px.bar(cleaned_df, x=cat_col, y=num_col, title=f'{cat_col}下{num_col}对比',
                                    color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                                    template='plotly_white')
                        st.plotly_chart(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 数值列相关性
        if len(selected_numeric_cols) >= 2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('数值列相关性')
            corr_matrix = cleaned_df[selected_numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, title='相关性热力图',
                           color_continuous_scale=['#e8f5e8', '#4caf50', '#2e7d32'],
                           template='plotly_white')
            st.plotly_chart(fig)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        # 行业看板功能
        st.subheader(f'{industry}行业数据分析')
        
        # 动态识别数据列
        numeric_cols = cleaned_df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = cleaned_df.select_dtypes(include=['object']).columns.tolist()
        
        # 自动检测日期列
        date_cols = []
        for col in cleaned_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['日期', '时间', 'month', 'date', 'time']):
                date_cols.append(col)
        
        # 1. 类别对比柱状图（如果有分类列和数值列）
        if categorical_cols and numeric_cols:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('类别对比分析')
            # 选择第一个分类列和数值列进行分析
            cat_col = categorical_cols[0]
            # 限制类别数量，避免图表过于拥挤
            if cleaned_df[cat_col].nunique() <= 10:
                for num_col in numeric_cols[:3]:  # 最多显示3个数值列
                    fig = px.bar(cleaned_df, x=cat_col, y=num_col, 
                                title=f'{cat_col}下{num_col}对比',
                                color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                                template='plotly_white')
                    st.plotly_chart(fig)
            else:
                st.write(f'{cat_col}类别数量过多（{cleaned_df[cat_col].nunique()}个），无法显示完整对比')
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 2. 数值列相关性热力图（如果有多列数值）
        if len(numeric_cols) >= 2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('数值列相关性分析')
            corr_matrix = cleaned_df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, title='相关性热力图',
                           color_continuous_scale=['#e8f5e8', '#4caf50', '#2e7d32'],
                           template='plotly_white')
            st.plotly_chart(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 3. 趋势图（如果有日期列和数值列）
        if date_cols and numeric_cols:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('时间趋势分析')
            date_col = date_cols[0]
            for num_col in numeric_cols[:3]:  # 最多显示3个数值列
                fig = px.line(cleaned_df, x=date_col, y=num_col, 
                            title=f'{num_col}随{date_col}趋势',
                            color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                            template='plotly_white')
                st.plotly_chart(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 4. 数据概览
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader('数据概览')
        st.write(f'数据形状：{cleaned_df.shape}')
        st.write(f'数值列：{numeric_cols}')
        st.write(f'分类列：{categorical_cols}')
        st.write(f'日期列：{date_cols}')
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 智能洞察板块
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader('智能洞察')
        st.write('💡 基于数据分析的业务建议')
        
        # 零售行业洞察
        if industry == '零售':
            # 漏斗转化率分析
            funnel_cols = ['浏览用户', '加购用户', '下单用户', '支付用户']
            if all(col in cleaned_df.columns for col in funnel_cols):
                funnel_values = [cleaned_df[col].sum() for col in funnel_cols]
                for i in range(len(funnel_values)-1):
                    conversion_rate = (funnel_values[i+1] / funnel_values[i]) * 100
                    if conversion_rate < 20:
                        st.write(f'💡 {funnel_cols[i]}到{funnel_cols[i+1]}的转化率偏低（{conversion_rate:.1f}%），建议优化相应流程')
            
            # 销售额日期分析
            if '日期' in cleaned_df.columns and '销售额' in cleaned_df.columns:
                max_sales_date = cleaned_df.loc[cleaned_df['销售额'].idxmax(), '日期']
                min_sales_date = cleaned_df.loc[cleaned_df['销售额'].idxmin(), '日期']
                st.write(f'💡 销售额最高的日期是{max_sales_date}，可能是促销活动影响')
                st.write(f'💡 销售额最低的日期是{min_sales_date}，建议分析原因')
            
            # 品类分析
            if '品类' in cleaned_df.columns and '销售额' in cleaned_df.columns:
                top_category = cleaned_df.groupby('品类')['销售额'].sum().idxmax()
                st.write(f'💡 销售额最高的品类是{top_category}，建议增加该品类的曝光')
            
            # 趋势分析
            if '日期' in cleaned_df.columns and '销售额' in cleaned_df.columns:
                # 简单趋势判断
                cleaned_df['日期'] = pd.to_datetime(cleaned_df['日期'])
                cleaned_df_sorted = cleaned_df.sort_values('日期')
                if len(cleaned_df_sorted) > 1:
                    first_half = cleaned_df_sorted.iloc[:len(cleaned_df_sorted)//2]['销售额'].mean()
                    second_half = cleaned_df_sorted.iloc[len(cleaned_df_sorted)//2:]['销售额'].mean()
                    if second_half > first_half:
                        st.write('💡 销售额整体呈上升趋势，建议保持当前策略')
                    else:
                        st.write('💡 销售额整体呈下降趋势，建议调整营销策略')
        
        # 制造业洞察
        elif industry == '制造业':
            # 生产量趋势分析
            if '日期' in cleaned_df.columns and '生产量' in cleaned_df.columns:
                cleaned_df['日期'] = pd.to_datetime(cleaned_df['日期'])
                cleaned_df_sorted = cleaned_df.sort_values('日期')
                if len(cleaned_df_sorted) > 1:
                    first_half = cleaned_df_sorted.iloc[:len(cleaned_df_sorted)//2]['生产量'].mean()
                    second_half = cleaned_df_sorted.iloc[len(cleaned_df_sorted)//2:]['生产量'].mean()
                    if second_half > first_half:
                        st.write('💡 生产量整体呈上升趋势，建议合理安排生产计划')
                    else:
                        st.write('💡 生产量整体呈下降趋势，建议分析原因并调整')
            
            # 设备故障分析
            if '设备名称' in cleaned_df.columns and '故障次数' in cleaned_df.columns:
                top_faulty_device = cleaned_df.groupby('设备名称')['故障次数'].sum().idxmax()
                st.write(f'💡 故障次数最多的设备是{top_faulty_device}，建议加强维护')
            
            # 质量合格率分析
            if '合格品数量' in cleaned_df.columns and '不合格品数量' in cleaned_df.columns:
                total = cleaned_df['合格品数量'].sum() + cleaned_df['不合格品数量'].sum()
                pass_rate = (cleaned_df['合格品数量'].sum() / total) * 100
                if pass_rate < 90:
                    st.write(f'💡 质量合格率偏低（{pass_rate:.1f}%），建议加强质量控制')
                else:
                    st.write(f'💡 质量合格率良好（{pass_rate:.1f}%），继续保持')
        
        # 科技行业洞察
        elif industry == '科技行业':
            # 用户增长趋势分析
            if '日期' in cleaned_df.columns and '新增用户数' in cleaned_df.columns:
                cleaned_df['日期'] = pd.to_datetime(cleaned_df['日期'])
                cleaned_df_sorted = cleaned_df.sort_values('日期')
                if len(cleaned_df_sorted) > 1:
                    first_half = cleaned_df_sorted.iloc[:len(cleaned_df_sorted)//2]['新增用户数'].mean()
                    second_half = cleaned_df_sorted.iloc[len(cleaned_df_sorted)//2:]['新增用户数'].mean()
                    if second_half > first_half:
                        st.write('💡 用户增长呈上升趋势，建议加大推广力度')
                    else:
                        st.write('💡 用户增长呈下降趋势，建议优化产品体验')
            
            # Bug 趋势分析
            if '日期' in cleaned_df.columns and 'Bug数量' in cleaned_df.columns:
                cleaned_df['日期'] = pd.to_datetime(cleaned_df['日期'])
                cleaned_df_sorted = cleaned_df.sort_values('日期')
                if len(cleaned_df_sorted) > 1:
                    first_half = cleaned_df_sorted.iloc[:len(cleaned_df_sorted)//2]['Bug数量'].mean()
                    second_half = cleaned_df_sorted.iloc[len(cleaned_df_sorted)//2:]['Bug数量'].mean()
                    if second_half < first_half:
                        st.write('💡 Bug数量呈下降趋势，代码质量正在改善')
                    else:
                        st.write('💡 Bug数量呈上升趋势，建议加强代码审查')
            
            # 渠道分析
            if '渠道' in cleaned_df.columns and '用户数' in cleaned_df.columns:
                top_channel = cleaned_df.groupby('渠道')['用户数'].sum().idxmax()
                st.write(f'💡 用户来源最多的渠道是{top_channel}，建议加大该渠道的投入')
        
        # 广告投放行业洞察
        elif industry == '广告投放行业':
            # ROI 分析
            if '渠道' in cleaned_df.columns and '花费' in cleaned_df.columns and '收入' in cleaned_df.columns:
                cleaned_df['ROI'] = (cleaned_df['收入'] - cleaned_df['花费']) / cleaned_df['花费'] * 100
                avg_roi = cleaned_df['ROI'].mean()
                if avg_roi < 100:
                    st.write(f'💡 平均 ROI 偏低（{avg_roi:.1f}%），建议优化广告投放策略')
                else:
                    st.write(f'💡 平均 ROI 良好（{avg_roi:.1f}%），继续保持')
            
            # 转化成本分析
            if '系列名称' in cleaned_df.columns and '转化成本' in cleaned_df.columns:
                top_campaign = cleaned_df.loc[cleaned_df['转化成本'].idxmin(), '系列名称']
                st.write(f'💡 转化成本最低的广告系列是{top_campaign}，建议参考其投放策略')
            
            # CTR 分析
            if '曝光量' in cleaned_df.columns and '点击量' in cleaned_df.columns:
                cleaned_df['CTR'] = (cleaned_df['点击量'] / cleaned_df['曝光量']) * 100
                avg_ctr = cleaned_df['CTR'].mean()
                if avg_ctr < 2:
                    st.write(f'💡 平均 CTR 偏低（{avg_ctr:.2f}%），建议优化广告创意')
                else:
                    st.write(f'💡 平均 CTR 良好（{avg_ctr:.2f}%），继续保持')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        # 下载按钮
        st.subheader('下载清洗后数据')
        # 生成 CSV 文件
        csv = cleaned_df.to_csv(index=False)
        st.download_button(
            label='下载 CSV 文件',
            data=csv,
            file_name='cleaned_data.csv',
            mime='text/csv'
        )
        
        # 生成 Excel 文件
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            cleaned_df.to_excel(writer, index=False, sheet_name='Cleaned Data')
        output.seek(0)
        st.download_button(
            label='下载 Excel 文件',
            data=output,
            file_name='cleaned_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # 右侧主区域（暂时空白，后续添加分析内容）
    st.subheader('分析区域')
    st.write('请先上传文件以进行数据分析...')

# 自然语言问答功能
if uploaded_file is not None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader('智能问答')
    # 初始化对话历史
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 显示对话历史
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.write(message['content'])
    
    # 聊天输入框
    user_input = st.chat_input('请输入您的问题，例如：总销售额是多少？')
    
    if user_input:
        # 添加用户消息到对话历史
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        # 构建数据上下文
        # 计算数值列统计信息
        numeric_stats = ""
        numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            numeric_stats = "\n数值列统计信息：\n"
            for col in numeric_cols:
                col_sum = cleaned_df[col].sum()
                col_mean = cleaned_df[col].mean()
                col_max = cleaned_df[col].max()
                col_min = cleaned_df[col].min()
                numeric_stats += f"- {col}: 总和={col_sum:.2f}, 均值={col_mean:.2f}, 最大值={col_max:.2f}, 最小值={col_min:.2f}\n"
        
        # 文本列示例
        text_samples = ""
        text_cols = cleaned_df.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            text_samples = "\n文本列示例：\n"
            for col in text_cols:
                unique_values = cleaned_df[col].dropna().unique()[:3]
                text_samples += f"- {col}: {list(unique_values)}\n"
        
        data_summary = f"""
数据摘要：
- 数据形状：{cleaned_df.shape}
- 列名：{list(cleaned_df.columns)}
{numeric_stats}
{text_samples}
"""
        
        # 系统提示词
        system_prompt = "你是一个数据分析助手，根据用户提供的数据信息回答业务问题。如果问题超出数据范围，请友好说明。"
        
        # 获取 API Key
        deepseek_api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        
        if not deepseek_api_key:
            response = "请在侧边栏配置 DeepSeek API Key 以使用智能问答功能。"
        else:
            try:
                # 构建 API 请求
                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {deepseek_api_key}"
                }
                
                # 构建消息列表
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"数据信息：{data_summary}\n用户问题：{user_input}"}
                ]
                
                # 发送请求
                payload = {
                    "model": "deepseek-chat",
                    "messages": messages,
                    "temperature": 0.7
                }
                
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                
                # 解析响应
                result = response.json()
                response = result['choices'][0]['message']['content']
                
            except Exception as e:
                response = f"API 调用失败：{str(e)}\n请检查 API Key 是否正确。"
        
        # 添加机器人回复到对话历史
        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        
        # 显示新的回复
        with st.chat_message('assistant'):
            st.write(response)
    st.markdown('</div>', unsafe_allow_html=True)
