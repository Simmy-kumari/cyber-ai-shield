import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

def preprocess(train_path,test_path):

    train = pd.read_csv(train_path, header=None, sep="\t")
    test = pd.read_csv(test_path, header=None, sep="\t")

    columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files",
    "num_outbound_cmds","is_host_login","is_guest_login","count",
    "srv_count","serror_rate","srv_serror_rate","rerror_rate",
    "srv_rerror_rate","same_srv_rate","diff_srv_rate",
    "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label","difficulty"
    ]

    train.columns = columns
    test.columns = columns[:-1]

    train['label'] = train['label'].apply(lambda x: 0 if x.lower()=="normal" else 1)
    test['label'] = test['label'].apply(lambda x: 0 if x.lower()=="normal" else 1)

    X_train = train.drop(["label","difficulty"],axis=1)
    y_train = train["label"]

    X_test = test.drop(["label"],axis=1)
    y_test = test["label"]

    X_train = pd.get_dummies(X_train)
    X_test = pd.get_dummies(X_test)

    # FIXED ALIGN
    X_train,X_test = X_train.align(X_test,join="outer",axis=1,fill_value=0)

    # Save columns
    joblib.dump(X_train.columns.tolist(),"models/reference_columns.pkl")

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    joblib.dump(scaler,"models/scaler.pkl")

    return X_train,y_train,X_test,y_test