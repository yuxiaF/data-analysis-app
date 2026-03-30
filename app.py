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
    
    # 行业选择下拉框
    with st.sidebar:
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.header('行业选择')
        industry = st.selectbox(
            '请选择行业',
            ['零售', '制造业', '科技行业', '广告投放行业']
        )
        
        # 筛选器
        st.header('数据筛选')
        # 第一个下拉框：所属板块
        if '所属板块' in cleaned_df.columns:
            sections = cleaned_df['所属板块'].dropna().unique().tolist()
            selected_section = st.selectbox('选择所属板块', ['全部'] + sections, key='section_selector')
        else:
            selected_section = '全部'
            st.write('数据中缺少"所属板块"列')
        
        # 第二个下拉框：当前门店名称（根据所选板块过滤）
        store_cols = [col for col in cleaned_df.columns if '门店' in col or '店' in col]
        if store_cols:
            store_col = store_cols[0]
            if selected_section != '全部' and '所属板块' in cleaned_df.columns:
                filtered_stores = cleaned_df[cleaned_df['所属板块'] == selected_section][store_col].dropna().unique().tolist()
            else:
                filtered_stores = cleaned_df[store_col].dropna().unique().tolist()
            selected_store = st.selectbox('选择门店', ['全部'] + filtered_stores, key='store_selector')
        else:
            selected_store = '全部'
            st.write('数据中缺少门店相关列')
        
        # 第三个下拉框：Fellow名（根据所选门店过滤）
        fellow_cols = [col for col in cleaned_df.columns if 'fellow' in col.lower() or 'Fellow' in col]
        if fellow_cols:
            fellow_col = fellow_cols[0]
            if selected_store != '全部' and store_cols:
                filtered_fellows = cleaned_df[cleaned_df[store_cols[0]] == selected_store][fellow_col].dropna().unique().tolist()
            elif selected_section != '全部' and '所属板块' in cleaned_df.columns:
                filtered_fellows = cleaned_df[cleaned_df['所属板块'] == selected_section][fellow_col].dropna().unique().tolist()
            else:
                filtered_fellows = cleaned_df[fellow_col].dropna().unique().tolist()
            selected_fellow = st.selectbox('选择Fellow', ['全部'] + filtered_fellows, key='fellow_selector')
        else:
            selected_fellow = '全部'
            st.write('数据中缺少Fellow相关列')
        
        # 指标选择
        numeric_cols = cleaned_df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            selected_metric = st.selectbox('选择指标', numeric_cols, index=numeric_cols.index('锁单') if '锁单' in numeric_cols else 0, key='metric_selector')
        else:
            selected_metric = '锁单'
            st.write('数据中缺少数值列')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 创建标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['数据清洗', '可视化看板', '行业看板', '绩效对比', '数据下载'])
    
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
                st.plotly_chart(fig, key=f"histogram_{col}")
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
                    st.plotly_chart(fig, key=f"trend_{col}")
            else:
                # 用行号作为X轴
                for col in selected_numeric_cols:
                    fig = px.line(cleaned_df, x=cleaned_df.index, y=col, title=f'{col}趋势',
                                 color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                                 template='plotly_white')
                    st.plotly_chart(fig, key=f"trend_no_date_{col}")
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
                        st.plotly_chart(fig, key=f"category_{cat_col}_{num_col}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 数值列相关性
        if len(selected_numeric_cols) >= 2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('数值列相关性')
            corr_matrix = cleaned_df[selected_numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, title='相关性热力图',
                           color_continuous_scale=['#e8f5e8', '#4caf50', '#2e7d32'],
                           template='plotly_white')
            st.plotly_chart(fig, key="correlation_heatmap")
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
                    st.plotly_chart(fig, key=f"industry_category_{cat_col}_{num_col}")
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
            st.plotly_chart(fig, key="industry_correlation_heatmap")
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
                st.plotly_chart(fig, key=f"industry_trend_{num_col}")
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
        
        # 板块层面洞察
        if '所属板块' in cleaned_df.columns and selected_metric in cleaned_df.columns:
            section_data = cleaned_df.groupby('所属板块')[selected_metric].sum().sort_values(ascending=False)
            if not section_data.empty:
                top_section = section_data.idxmax()
                top_value = section_data.max()
                st.write(f'💡 {top_section}{selected_metric}总量最高，建议作为标杆推广。')
                
                # 板块间对比
                if len(section_data) > 1:
                    avg_value = section_data.mean()
                    below_avg_sections = section_data[section_data < avg_value].index.tolist()
                    if below_avg_sections:
                        st.write(f'💡 {"、".join(below_avg_sections)}板块{selected_metric}低于平均水平，建议分析原因并改进。')
        
        # 门店层面洞察
        store_cols = [col for col in cleaned_df.columns if '门店' in col or '店' in col]
        if store_cols and selected_metric in cleaned_df.columns:
            store_col = store_cols[0]
            if selected_section != '全部' and '所属板块' in cleaned_df.columns:
                store_data = cleaned_df[cleaned_df['所属板块'] == selected_section].groupby(store_col)[selected_metric].sum().sort_values(ascending=False)
            else:
                store_data = cleaned_df.groupby(store_col)[selected_metric].sum().sort_values(ascending=False)
            
            if not store_data.empty:
                top_store = store_data.idxmax()
                top_store_value = store_data.max()
                st.write(f'💡 {top_store}{selected_metric}最高，建议总结其成功经验。')
                
                # 净锁单转化率分析
                if '净锁单' in cleaned_df.columns and '锁单' in cleaned_df.columns:
                    if selected_section != '全部' and '所属板块' in cleaned_df.columns:
                        section_stores = cleaned_df[cleaned_df['所属板块'] == selected_section][store_col].unique()
                        store_conversion = {}
                        for store in section_stores:
                            store_df = cleaned_df[(cleaned_df[store_col] == store) & (cleaned_df['所属板块'] == selected_section)]
                            if not store_df.empty and store_df['锁单'].sum() > 0:
                                conversion = (store_df['净锁单'].sum() / store_df['锁单'].sum()) * 100
                                store_conversion[store] = conversion
                        
                        if store_conversion:
                            avg_conversion = sum(store_conversion.values()) / len(store_conversion)
                            low_conversion_stores = [store for store, conv in store_conversion.items() if conv < avg_conversion * 0.8]
                            if low_conversion_stores:
                                st.write(f'💡 {"、".join(low_conversion_stores)}净锁单转化率低于同板块其他门店，建议优化跟进流程。')
        
        # 个人层面洞察
        fellow_cols = [col for col in cleaned_df.columns if 'fellow' in col.lower() or 'Fellow' in col]
        if fellow_cols and selected_metric in cleaned_df.columns:
            fellow_col = fellow_cols[0]
            if selected_store != '全部' and store_cols:
                fellow_data = cleaned_df[cleaned_df[store_cols[0]] == selected_store].groupby(fellow_col)[selected_metric].sum().sort_values(ascending=False)
                # 计算门店平均值
                store_avg = cleaned_df[cleaned_df[store_cols[0]] == selected_store][selected_metric].mean()
                comparison_label = f'{selected_store}均值'
            elif selected_section != '全部' and '所属板块' in cleaned_df.columns:
                fellow_data = cleaned_df[cleaned_df['所属板块'] == selected_section].groupby(fellow_col)[selected_metric].sum().sort_values(ascending=False)
                # 计算板块平均值
                store_avg = cleaned_df[cleaned_df['所属板块'] == selected_section][selected_metric].mean()
                comparison_label = f'{selected_section}均值'
            else:
                fellow_data = cleaned_df.groupby(fellow_col)[selected_metric].sum().sort_values(ascending=False)
                # 计算整体平均值
                store_avg = cleaned_df[selected_metric].mean()
                comparison_label = '整体均值'
            
            if not fellow_data.empty:
                top_fellow = fellow_data.idxmax()
                top_fellow_value = fellow_data.max()
                if top_fellow_value > store_avg * 1.2:
                    st.write(f'💡 {top_fellow}{selected_metric}量远超{comparison_label}，建议分享经验。')
                
                # 识别表现较差的Fellow
                low_performers = fellow_data[fellow_data < store_avg * 0.8].index.tolist()
                if low_performers:
                    st.write(f'💡 {"、".join(low_performers)}{selected_metric}量低于{comparison_label}，建议提供培训和支持。')
        
        # 行业特定洞察
        # 零售行业洞察
        if industry == '零售':
            # 检查数据中是否存在相关列
            has_lock = '锁单' in cleaned_df.columns
            has_net_lock = '净锁单' in cleaned_df.columns
            
            # 锁单→净锁单转化率分析
            if has_lock and has_net_lock:
                total_lock = cleaned_df['锁单'].sum()
                total_net_lock = cleaned_df['净锁单'].sum()
                if total_lock > 0:
                    conversion_rate = (total_net_lock / total_lock) * 100
                    st.write(f'💡 锁单→净锁单转化率为{conversion_rate:.1f}%，')
                    if conversion_rate < 80:
                        st.write('💡 转化率偏低，建议优化销售流程，减少订单流失')
                    else:
                        st.write('💡 转化率良好，继续保持')
            
            # 漏斗转化率分析（如果存在传统漏斗列）
            funnel_cols = ['浏览用户', '加购用户', '下单用户', '支付用户']
            if all(col in cleaned_df.columns for col in funnel_cols):
                funnel_values = [cleaned_df[col].sum() for col in funnel_cols]
                for i in range(len(funnel_values)-1):
                    conversion_rate = (funnel_values[i+1] / funnel_values[i]) * 100
                    if conversion_rate < 20:
                        st.write(f'💡 {funnel_cols[i]}到{funnel_cols[i+1]}的转化率偏低（{conversion_rate:.1f}%），建议优化相应流程')
            
            # 销售额分析（如果存在销售额列）
            if '日期' in cleaned_df.columns and '销售额' in cleaned_df.columns:
                max_sales_date = cleaned_df.loc[cleaned_df['销售额'].idxmax(), '日期']
                min_sales_date = cleaned_df.loc[cleaned_df['销售额'].idxmin(), '日期']
                st.write(f'💡 销售额最高的日期是{max_sales_date}，可能是促销活动影响')
                st.write(f'💡 销售额最低的日期是{min_sales_date}，建议分析原因')
            
            # 品类分析（如果存在品类列）
            if '品类' in cleaned_df.columns and '销售额' in cleaned_df.columns:
                top_category = cleaned_df.groupby('品类')['销售额'].sum().idxmax()
                st.write(f'💡 销售额最高的品类是{top_category}，建议增加该品类的曝光')
            
            # 趋势分析（如果存在日期和销售额列）
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
        # 绩效对比标签页
        st.subheader('绩效对比分析')
        
        # 板块对比柱状图
        if '所属板块' in cleaned_df.columns and selected_metric in cleaned_df.columns:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('板块对比分析')
            section_data = cleaned_df.groupby('所属板块')[selected_metric].sum().reset_index()
            fig = px.bar(section_data, x='所属板块', y=selected_metric, 
                        title=f'各板块{selected_metric}总和',
                        color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                        template='plotly_white')
            st.plotly_chart(fig, key="section_comparison")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 门店对比柱状图
        store_cols = [col for col in cleaned_df.columns if '门店' in col or '店' in col]
        if store_cols and selected_metric in cleaned_df.columns:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('门店对比分析')
            store_col = store_cols[0]
            if selected_section != '全部' and '所属板块' in cleaned_df.columns:
                store_data = cleaned_df[cleaned_df['所属板块'] == selected_section].groupby(store_col)[selected_metric].sum().reset_index()
                title = f'{selected_section}板块下各门店{selected_metric}总和'
            else:
                store_data = cleaned_df.groupby(store_col)[selected_metric].sum().reset_index()
                title = f'各门店{selected_metric}总和'
            fig = px.bar(store_data, x=store_col, y=selected_metric, 
                        title=title,
                        color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                        template='plotly_white')
            st.plotly_chart(fig, key="store_comparison")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 个人对比柱状图
        fellow_cols = [col for col in cleaned_df.columns if 'fellow' in col.lower() or 'Fellow' in col]
        if fellow_cols and selected_metric in cleaned_df.columns:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader('个人对比分析')
            fellow_col = fellow_cols[0]
            if selected_store != '全部' and store_cols:
                fellow_data = cleaned_df[cleaned_df[store_cols[0]] == selected_store].groupby(fellow_col)[selected_metric].sum().reset_index()
                title = f'{selected_store}门店下各Fellow{selected_metric}量'
                # 计算门店平均值
                store_avg = cleaned_df[cleaned_df[store_cols[0]] == selected_store][selected_metric].mean()
            elif selected_section != '全部' and '所属板块' in cleaned_df.columns:
                fellow_data = cleaned_df[cleaned_df['所属板块'] == selected_section].groupby(fellow_col)[selected_metric].sum().reset_index()
                title = f'{selected_section}板块下各Fellow{selected_metric}量'
                # 计算板块平均值
                store_avg = cleaned_df[cleaned_df['所属板块'] == selected_section][selected_metric].mean()
            else:
                fellow_data = cleaned_df.groupby(fellow_col)[selected_metric].sum().reset_index()
                title = f'各Fellow{selected_metric}量'
                # 计算整体平均值
                store_avg = cleaned_df[selected_metric].mean()
            
            fig = px.bar(fellow_data, x=fellow_col, y=selected_metric, 
                        title=title,
                        color_discrete_sequence=['#4caf50', '#2196f3', '#ff9800'],
                        template='plotly_white')
            # 添加平均水平线
            fig.add_hline(y=store_avg, line_dash="dash", line_color="red", 
                         annotation_text=f"平均值: {store_avg:.2f}",
                         annotation_position="top right")
            st.plotly_chart(fig, key="fellow_comparison")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 个人工作详情
        if fellow_cols and selected_fellow != '全部':
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f'{selected_fellow}工作详情')
            fellow_col = fellow_cols[0]
            # 筛选该Fellow的数据
            fellow_detail = cleaned_df[cleaned_df[fellow_col] == selected_fellow]
            
            if not fellow_detail.empty:
                # 选择需要展示的指标
                metrics = ['锁单', '净锁单', '交付', 'Call量15s', '外呼时长min']
                metrics = [m for m in metrics if m in cleaned_df.columns]
                
                if metrics:
                    # 计算Fellow的指标值
                    fellow_metrics = {}
                    for metric in metrics:
                        fellow_metrics[metric] = fellow_detail[metric].sum()
                    
                    # 计算门店或板块的均值
                    if selected_store != '全部' and store_cols:
                        avg_metrics = {}
                        for metric in metrics:
                            avg_metrics[metric] = cleaned_df[cleaned_df[store_cols[0]] == selected_store][metric].mean()
                        comparison_label = f'{selected_store}均值'
                    elif selected_section != '全部' and '所属板块' in cleaned_df.columns:
                        avg_metrics = {}
                        for metric in metrics:
                            avg_metrics[metric] = cleaned_df[cleaned_df['所属板块'] == selected_section][metric].mean()
                        comparison_label = f'{selected_section}均值'
                    else:
                        avg_metrics = {}
                        for metric in metrics:
                            avg_metrics[metric] = cleaned_df[metric].mean()
                        comparison_label = '整体均值'
                    
                    # 准备数据用于横向条形图
                    metric_data = []
                    for metric in metrics:
                        metric_data.append({'指标': metric, '数值': fellow_metrics[metric], '类型': selected_fellow})
                        metric_data.append({'指标': metric, '数值': avg_metrics[metric], '类型': comparison_label})
                    
                    # 创建横向条形图
                    fig = px.bar(pd.DataFrame(metric_data), x='数值', y='指标', color='类型', 
                                barmode='group',
                                title=f'{selected_fellow}与{comparison_label}对比',
                                color_discrete_sequence=['#4caf50', '#2196f3'],
                                template='plotly_white')
                    st.plotly_chart(fig, key="fellow_detail")
                else:
                    st.write('数据中缺少相关指标列')
            else:
                st.write(f'未找到{selected_fellow}的相关数据')
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
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
        
        # 本地查询预处理：处理"某门店锁单总和"类型的问题
        response = None
        import re
        # 匹配模式："[门店名称]锁单总和" 或 "锁单总和[门店名称]"
        store_pattern = re.compile(r'(.*?)(锁单总和|锁单总金额|锁单总计)(.*?)')
        match = store_pattern.search(user_input)
        
        if match:
            # 提取门店名称
            store_name = match.group(1).strip() + match.group(3).strip()
            # 检查是否存在门店列和锁单列
            store_cols = [col for col in cleaned_df.columns if '门店' in col or '店' in col]
            if store_cols and '锁单' in cleaned_df.columns:
                store_col = store_cols[0]
                # 筛选特定门店的锁单数据
                if store_name:
                    store_data = cleaned_df[cleaned_df[store_col].str.contains(store_name, na=False)]
                    if not store_data.empty:
                        lock_sum = store_data['锁单'].sum()
                        response = f"{store_name}的锁单总和为{lock_sum:.2f}"
                    else:
                        response = f"未找到名称包含'{store_name}'的门店"
                else:
                    # 如果没有指定门店，计算所有门店的锁单总和
                    total_lock = cleaned_df['锁单'].sum()
                    response = f"所有门店的锁单总和为{total_lock:.2f}"
        
        # 如果本地处理未返回结果，调用 API
        if response is None:
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
            
            # 按板块汇总锁单信息
            section_aggregation = ""
            if '所属板块' in cleaned_df.columns and '锁单' in cleaned_df.columns:
                section_summary = cleaned_df.groupby('所属板块')['锁单'].sum().sort_values(ascending=False)
                section_aggregation = "\n按板块汇总锁单：\n"
                for section, lock_sum in section_summary.items():
                    section_aggregation += f"- {section}: {lock_sum:.2f}\n"
            
            # 门店名称列表（如果数量不多）
            store_list = ""
            store_cols = [col for col in cleaned_df.columns if '门店' in col or '店' in col]
            if store_cols:
                store_col = store_cols[0]
                stores = cleaned_df[store_col].dropna().unique()
                if len(stores) <= 20:  # 限制门店数量，避免摘要过长
                    store_list = "\n门店名称列表：\n"
                    store_list += f"- {', '.join(stores)}"
                else:
                    store_list = f"\n门店数量：{len(stores)}个（数量较多，不列出具体名称）"
            
            data_summary = f"""
数据摘要：
- 数据形状：{cleaned_df.shape}
- 列名：{list(cleaned_df.columns)}
{numeric_stats}
{text_samples}
{section_aggregation}
{store_list}
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
