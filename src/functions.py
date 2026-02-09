import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.stats import chi2_contingency

def print_unique_values_summary(df, columns):
    """
    Gibt eine Zusammenfassung der eindeutigen Werte pro Spalte im DataFrame aus.
    """

    for col in columns: # Iteriere über die angegebenen Spalten
        print(f"=== {col} ===")
        print(f"Eindeutige Werte: {df[col].nunique()}")
        print(f"Fehlende Werte: {df[col].isna().sum():,}")
        print("\nTop 10 häufigste Werte:")

        counts = df[col].value_counts().head(10) # Zähle die häufigsten Werte
        for val, count in counts.items():
            pct = (count / len(df) * 100) # Berechne den Prozentsatz
            print(f"'{val}' - {count:,} - {pct:.2f}%") # Ausgabe des Werts, der Anzahl und dem Prozentsatz
        print("\n")

def save_unique_values_summary(df, columns, df_name):
    """
    Speichert eine Zusammenfassung der eindeutigen Werte pro Spalte im DataFrame in einer Textdatei.
    """

    output_lines = [f'Zusammenfassung der eindeutigen Werte pro Spalte in {df_name}']
    output_lines.append("=" * 60)
    output_lines.append("")

    for column in columns:
        if column in df.columns:
            # Zähle eindeutige Werte und deren Häufigkeiten
            value_counts = df[column].value_counts()
            total_count = len(df)
            
            output_lines.append(f"Spalte: {column}")
            output_lines.append(f"Anzahl eindeutiger Werte: {len(value_counts)}")
            output_lines.append("Wert - Anzahl - Prozent")
            
            for value, count in value_counts.items():
                percentage = (count / total_count) * 100
                output_lines.append(f"'{value}' - {count} - {percentage:.2f}%")
            
            # Füge NaN-Zählung hinzu
            nan_count = df[column].isna().sum()
            if nan_count > 0:
                nan_percentage = (nan_count / total_count) * 100
                output_lines.append(f"NaN - {nan_count} - {nan_percentage:.2f}%")
            
            output_lines.append("")
            output_lines.append("-" * 60)
            output_lines.append("")

    output_dir = 'outputs'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Speichere in Datei
    output_file_path = f'{output_dir}/{df_name}_unique_values_summary.txt'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"Datei erfolgreich gespeichert: {output_file_path}")




def plot_share_vs_conversion(df, column_name, size=(16, 8), color_share='lightgrey', color_cv='gold', sortby=['user_share', False]):
    """
    Erstellt ein Balkendiagramm, das den Benutzeranteil und die Conversion Rate für eine gegebene Spalte darstellt.
    """

    # Berechne die Zusammenfassung
    df_summary = df.groupby(column_name).agg(
        total_users = ('user_id', 'count'),
        booked_users = ('booked', 'sum')
    ).reset_index()
    df_summary['conversion_rate'] = round(df_summary['booked_users'] / df_summary['total_users'] * 100, 2)
    df_summary['user_share'] = round(df_summary['total_users'] / df_summary['total_users'].sum() * 100, 2)
    global_conversion = round(df_summary['booked_users'].sum() / df_summary['total_users'].sum() * 100, 2)

    df_summary = df_summary.sort_values(by=sortby[0], ascending=sortby[1])

    # Erstelle das Balkendiagramm
    fig, ax = plt.subplots(figsize=size)

    # Setze Achsenbeschriftungen
    ax.set_xlabel(column_name, fontsize=12)
    ax.set_ylabel('Anteil (%)', fontsize=12)
    ax.set_ylim(0, 100)

    # Zeichne die Balkendiagramme
    bar1 = ax.bar(df_summary[column_name], df_summary['user_share'], color=color_share, width=0.8, alpha=0.6, label='Anteil der Benutzer')
    bar2 = ax.bar(df_summary[column_name], df_summary['conversion_rate'], color=color_cv, width=0.3, alpha=0.6, label='Conversion Rate')
    ln1 = ax.axhline(y=global_conversion, color='tomato', linestyle='--', label='Durchschnittliche Conversion Rate')

    # Füge Datenbeschriftungen hinzu
    # ax.bar_label(bar1, fmt='%.2f%%', fontsize=9, color='dimgray')
    for p in bar1.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy() 
        ax.text(
            x, 
            y + height + 2, 
            f'{height:.1f}%', 
            horizontalalignment='left', 
            verticalalignment='top',
            color='grey',
            fontsize=8,
            fontweight='bold'
            )
    ax.bar_label(bar2, fmt='%.2f%%', padding=3, fontsize=9, weight='bold', color='dimgray')

    # Füge Legende und Formatierung hinzu
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(loc='upper right')

    # Ausgabe
    fig.suptitle(f'Benutzeranteil und Conversion Rate nach {column_name}', fontsize=16)
    fig.tight_layout()
    plt.show()










def categorical_correlation_analysis(df, var1, var2, min_sample=25):
    """
    Vollständige Korrelationsanalyse zwischen zwei kategorialen Spalten.
    """
    
    print("="*60)
    print(f"Korrelationsanalyse: {var1} vs {var2}")
    print("="*60)
    
    # 1. Basisinformationen
    print(f"\n1. Datenüberblick:")
    print(f"   {var1}: {df[var1].nunique()} eindeutige Werte")
    print(f"   {var2}: {df[var2].nunique()} eindeutige Werte")
    print(f"   Gesamtbeobachtungen: {len(df)}")
    
    # 2. Chi-Quadrat-Test
    ct = pd.crosstab(df[var1], df[var2])
    chi2, p, dof, expected = chi2_contingency(ct)
    
    print(f"\n2. Pearsons Chi-Quadrat-Test:")
    print(f"   χ² = {chi2:.2f}")
    print(f"   p-Wert = {p:.3f}")
    print(f"   Freiheitsgrade = {dof}")
    
    # 3. Interpretation
    print(f"\n3. Interpretation:")
    if p < 0.01:
        print(f"   Sehr hohe Signifikanz nachgewiesen (p < 0.01)")
    elif p < 0.05:
        print(f"   Hohe Signifikanz nachgewiesen (p < 0.05)")
    else:
        print(f"   Keine Signifikanz nachgewiesen (p ≥ 0.05)")
    
    # 4. Visualisierungen
    print(f"\n4. Visualisierung:")
    fig, ax = plt.subplots(3, 1, figsize=(20, 20))
    
    # Absolute Werte
    sns.heatmap(ct, fmt='d', annot=True, cmap='Blues', ax=ax[0], cbar_kws={'label': 'Häufigkeit'})
    ax[0].set(
        title=f'Absolute Häufigkeiten\n{var1} vs {var2}',
        xlabel=var2,
        ylabel=var1
    )
    
    # Normalisierte Werte (pro Zeile)
    normalized = ct.div(ct.sum(axis=1), axis=0)
    sns.heatmap(normalized, annot=True, fmt='.2%', cmap='YlOrRd', ax=ax[1], cbar_kws={'label': 'Prozent (%)'})
    ax[1].set(
        title=f'Normalisiert pro Zeile (%)\n{var1} vs {var2}',
        xlabel=var2,
        ylabel=var1
    )
    
    # Affinitäten
    global_avg = ct.sum(axis=0) / ct.sum().sum()
    lift_matrix = normalized.div(global_avg, axis=1)

    low_data_mask = ct < min_sample
    lift_matrix[low_data_mask] = np.nan

    sns.heatmap(lift_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=1.0, vmin=0.5, vmax=2.0, ax=ax[2], cbar_kws={'label': 'Affinität'})
    ax[2].set(
        title=f'Affinitäten\n{var1} vs {var2}',
        xlabel=var2,
        ylabel=var1
    )

    fig.suptitle(f'Zusammenhangsanalyse: {var1} und {var2} | χ²={chi2:.1f}, p={p:.3f}', 
                 fontsize=14, y=1.02)
    fig.tight_layout()
    plt.show()

    # Stärkste Assoziationen
    print(f"\n5. Stärkste Assoziationen:")
    
    # Finden der Maximalwerte in jeder Zeile
    for row in normalized.index:
        max_col = normalized.loc[row].idxmax()
        max_value = normalized.loc[row, max_col]
        print(f'    {row}: {max_col} ({max_value:.2%})')
    print('')