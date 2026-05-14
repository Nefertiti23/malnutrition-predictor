import pandas as pd
import pyreadstat

def make_combined(raw_path):

    # ---- BALOCHISTAN ----
    ch_bal, _ = pyreadstat.read_sav(f"{raw_path}/balochistan/ch_bal.sav")
    hh_bal, _ = pyreadstat.read_sav(f"{raw_path}/balochistan/hh_bal.sav")
    hl_bal, _ = pyreadstat.read_sav(f"{raw_path}/balochistan/hl_bal.sav")
    ch_bal["province"] = "Balochistan"
    hh_bal["province"] = "Balochistan"
    hl_bal["province"] = "Balochistan"

    # ---- KPK ----
    ch_kpk, _ = pyreadstat.read_sav(f"{raw_path}/kpk/ch_kpk.sav")
    hh_kpk, _ = pyreadstat.read_sav(f"{raw_path}/kpk/hh_kpk.sav")
    hl_kpk, _ = pyreadstat.read_sav(f"{raw_path}/kpk/hl_kpk.sav")
    ch_kpk["province"] = "KPK"
    hh_kpk["province"] = "KPK"
    hl_kpk["province"] = "KPK"

    # ---- SINDH ----
    ch_sindh, _ = pyreadstat.read_sav(f"{raw_path}/sindh/ch_sindh.sav")
    hh_sindh, _ = pyreadstat.read_sav(f"{raw_path}/sindh/hh_sindh.sav")
    hl_sindh, _ = pyreadstat.read_sav(f"{raw_path}/sindh/hl_sindh.sav")
    ch_sindh["province"] = "Sindh"
    hh_sindh["province"] = "Sindh"
    hl_sindh["province"] = "Sindh"

    # ---- COMBINE all 3 provinces ----
    ch_all = pd.concat([ch_bal, ch_kpk, ch_sindh], ignore_index=True)
    hh_all = pd.concat([hh_bal, hh_kpk, hh_sindh], ignore_index=True)
    hl_all = pd.concat([hl_bal, hl_kpk, hl_sindh], ignore_index=True)

    # ---- Save to CSV ----
    ch_all.to_csv(f"{raw_path}/ch_combined.csv", index=False)
    hh_all.to_csv(f"{raw_path}/hh_combined.csv", index=False)
    hl_all.to_csv(f"{raw_path}/hl_combined.csv", index=False)

def clean_ch(clean_path):
    ch = pd.read_csv(clean_path, low_memory=False)

    cols = ['HH1','HH2','CAGE','HL4','BR2','BR3','HAZ','WAZ',
        'WHZ','HAZ2','WAZ2','WHZ2','melevel','HH6','HH7',
        'windex5','cdisability','province']

    df = ch[cols].copy()

    df.columns = ['cluster_id','household_id','child_age_months','child_sex',
        'birth_weight','breastfeeding','haz_score','waz_score','whz_score',
        'stunted','underweight','wasted','mother_education','urban_rural',
        'district','wealth_index','disability','province']

    df['stunted']     = (df['stunted'] < -2).astype(int)
    df['wasted']      = (df['wasted'] < -2).astype(int)
    df['underweight'] = (df['underweight'] < -2).astype(int)

    df = df.dropna(subset=['child_age_months', 'haz_score'])
    df['birth_weight_known'] = df['birth_weight'].notna().astype(int)
    df = df.drop(columns=['birth_weight'])
    df['breastfeeding']    = df['breastfeeding'].fillna(df['breastfeeding'].mode()[0])
    df['disability']       = df['disability'].fillna(0)
    df['mother_education'] = df['mother_education'].fillna(df['mother_education'].mode()[0])

    df['child_sex']    = df['child_sex'].map({1.0: 0, 2.0: 1})
    df['urban_rural']  = df['urban_rural'].map({1.0: 0, 2.0: 1})
    df['province']     = df['province'].map({'Balochistan': 0, 'KPK': 1, 'Sindh': 2})

    return df

def clean_hh(clean_path):
    hh = pd.read_csv(clean_path, low_memory=False)

    cols_to_keep = [
        'HH1', 'HH2',          # Merge keys (Cluster & Household)
        'HC3',                 # Main material of the roof/walls (Housing Quality)
        'WS1',                 # Source of drinking water
        'WS8',                 # Type of toilet facility
        'helevel',             # Education level (Household head/generalized)
        'HH6',                 # Urban/Rural
        'HH7',                 # District
        'windex5',             # Wealth index
        'province'             # Province
    ]

    df = hh[cols_to_keep].copy()
    df.columns = [
        'cluster_id', 'household_id',
        'housing_quality', 'water_source',
        'sanitation_type', 'education_level',
        'urban_rural', 'district',
        'wealth_index', 'province'
    ]

    df['education_level'] = df['education_level'].fillna(df['education_level'].mode().iloc[0])
    df['sanitation_type'] = df['sanitation_type'].fillna(df['sanitation_type'].mode().iloc[0])
    df['housing_quality'] = df['housing_quality'].fillna(df['housing_quality'].mode().iloc[0])
    df['water_source']    = df['water_source'].fillna(df['water_source'].mode().iloc[0])

    df['urban_rural'] = df['urban_rural'].map({1.0: 0, 2.0: 1})
    df['province'] = df['province'].map({
        'Balochistan': 0,
        'KPK': 1,
        'Sindh': 2
    })

    return df

def clean_hl(clean_path):
    hl = pd.read_csv(clean_path, low_memory=False)

    cols_to_keep = [
        'HH1', 'HH2',           # Merge keys
        'HL4',                  # Child sex
        'HL6',                  # Age
        'melevel',              # Mother education
        'helevel',              # Household education
        'HH6',                  # Urban/Rural
        'HH7',                  # District
        'windex5',              # Wealth index
        'disability',           # Disability
        'province'              # Province
    ]
    df = hl[cols_to_keep].copy()

    df.columns = [
        'cluster_id', 'household_id',
        'child_sex', 'child_age_months',
        'mother_education', 'household_education',
        'urban_rural', 'district',
        'wealth_index', 'disability', 'province'
    ]

    df['disability'] = df['disability'].fillna(0)
    df['mother_education'] = df['mother_education'].fillna(
        df['mother_education'].mode()[0]
    )
    df['child_sex'] = df['child_sex'].map({1.0: 0, 2.0: 1})
    df['urban_rural'] = df['urban_rural'].map({1.0: 0, 2.0: 1})
    df['province'] = df['province'].map({
        'Balochistan': 0,
        'KPK': 1,
        'Sindh': 2
    })

    return df

def combine(ch, hh, hl):
    hh_clean = hh.drop(columns=['urban_rural', 'district', 'wealth_index', 'province'])
    hl_clean = hl.drop(columns=['child_sex', 'child_age_months', 'urban_rural',
                                  'district', 'wealth_index', 'province', 'disability'])

    merged = ch.merge(hh_clean, on=['cluster_id', 'household_id'], how='left')
    merged = merged.merge(hl_clean, on=['cluster_id', 'household_id'], how='left')

    merged = merged.drop_duplicates(subset=['cluster_id', 'household_id',
                                             'child_age_months', 'child_sex'])

    merged = merged.drop(columns=['mother_education_y'])
    merged = merged.rename(columns={'mother_education_x': 'mother_education'})

    return merged

def run_pipeline(raw_dir, output_path):
    ch = clean_ch(f"{raw_dir}/ch_combined.csv")
    hh = clean_hh(f"{raw_dir}/hh_combined.csv")
    hl = clean_hl(f"{raw_dir}/hl_combined.csv")

    final = combine(ch, hh, hl)

    final = final[(final['haz_score'] >= -6) & (final['haz_score'] <= 6)]
    final = final[(final['waz_score'] >= -6) & (final['waz_score'] <= 6)]
    final = final[(final['whz_score'] >= -6) & (final['whz_score'] <= 6)]

    final.to_csv(output_path, index=False)
    return final


if __name__ == "__main__":
    # make_combined("data/raw")
    run_pipeline("data/raw", "data/processed/final_dataset_clean.csv")