from __future__ import annotations

import copy
from abc import abstractmethod

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder, StandardScaler


class BaseTransform:

    def __init__(self):
        """Initialises the BaseTransform class."""
        super().__init__()
        self._is_fitted = False

    @property
    def is_fitted(self) -> bool:
        """Whether the transform is already fitted."""
        return self._is_fitted

    def fit(
        self,
        data_df: pd.DataFrame,
    ):
        """Fits the transform to the data.

        Args:
            data_df (pd.DataFrame): Data to fit the transform to.
        """
        self._fit(data_df)
        self._is_fitted = True

    def transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Transforms the data.

        Args:
            data_df (pd.DataFrame): Data to transform.

        Raises:
            ValueError: If the transform is not yet fitted.

        Returns:
            pd.DataFrame: Transformed data.
        """
        if not self.is_fitted:
            raise ValueError(
                f"'{self.__class__.__name__}' is not yet fitted ."
                f"Please run `fit()` first before attempting to "
                f"transform the DataFrame."
            )
        data_df_transformed = self._transform(copy.deepcopy(data_df))
        return data_df_transformed

    def inverse_transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Inverse transforms the data.

        Args:
            data_df (pd.DataFrame): Data to inverse transform.

        Raises:
            ValueError: If the transform is not yet fitted.

        Returns:
            pd.DataFrame: Inverse transformed data.
        """
        if not self.is_fitted:
            raise ValueError(
                f"'{self.__class__.__name__}' is not yet fitted ."
                f"Please run `fit()` first before attempting to "
                f"inverse transform the DataFrame."
            )
        data_df_inverse_transformed = self._inverse_transform(copy.deepcopy(data_df))

        return data_df_inverse_transformed

    @abstractmethod
    def _fit(
        self,
        data_df: pd.DataFrame,
    ):
        """Fits the transform to the data.

        Args:
            data_df (pd.DataFrame): Data to fit the transform to.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def _transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Transforms the data.

        Args:
            data_df (pd.DataFrame): Data to transform.

        Raises:
            NotImplementedError: If the method is not implemented.

        Returns:
            pd.DataFrame: Transformed data.
        """
        raise NotImplementedError

    @abstractmethod
    def _inverse_transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Inverse transforms the data.

        Args:
            data_df (pd.DataFrame): Data to inverse transform.

        Raises:
            NotImplementedError: If the method is not implemented.

        Returns:
            pd.DataFrame: Inverse transformed data.
        """
        raise NotImplementedError


class StandardiseTransform(BaseTransform):

    def __init__(
        self,
        copy: bool = True,
        with_mean: bool = True,
        with_std: bool = True,
    ):
        """Initialises the StandardiseTransform class.

        Args:
            The same as sklearn.preprocessing.StandardScaler.
        """
        super().__init__()
        self._scaler = StandardScaler(copy=copy, with_mean=with_mean, with_std=with_std)

    def _fit(
        self,
        data_df: pd.DataFrame,
    ):
        """Fits the transform to the data.

        Args:
            data_df (pd.DataFrame): Data to fit the transform to.
        """
        self._scaler.fit(data_df)

    def _transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Transforms the data.

        Args:
            data_df (pd.DataFrame): Data to transform.

        Returns:
            pd.DataFrame: Transformed data.
        """
        data_df_transformed = self._scaler.transform(data_df)
        return pd.DataFrame(data_df_transformed, columns=data_df.columns, index=data_df.index)

    def _inverse_transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Inverse transforms the data.

        Args:
            data_df (pd.DataFrame): Data to inverse transform.

        Returns:
            pd.DataFrame: Inverse transformed data.
        """
        data_df_inverse_transformed = self._scaler.inverse_transform(data_df)
        return pd.DataFrame(data_df_inverse_transformed, columns=data_df.columns, index=data_df.index)


class SimpleImputeTransform(BaseTransform):

    def __init__(
        self,
        categorical_feature_list: list,
        numerical_feature_list: list,
        strategy_categorical: str,
        strategy_numerical: str,
        missing_values=np.nan,
        fill_value=None,
        copy=True,
        add_indicator=False,
        keep_empty_features=False,
    ):

        super().__init__()

        # === Basic configurations ===
        self.categorical_feature_list = categorical_feature_list
        self.numerical_feature_list = numerical_feature_list

        # === Set the imputers for categorical and numerical features ===
        self._imputer_categotical = SimpleImputer(
            missing_values=missing_values,
            strategy=strategy_categorical,
            fill_value=fill_value,
            copy=copy,
            add_indicator=add_indicator,
            keep_empty_features=keep_empty_features,
        )
        self._imputer_numerical = SimpleImputer(
            missing_values=missing_values,
            strategy=strategy_numerical,
            fill_value=fill_value,
            copy=copy,
            add_indicator=add_indicator,
            keep_empty_features=keep_empty_features,
        )

    def _fit(
        self,
        data_df: pd.DataFrame,
    ):
        """Fits the transform to the data.

        Args:
            data_df (pd.DataFrame): Data to fit the transform to.
        """
        if self.categorical_feature_list:
            self._imputer_categotical.fit(data_df[self.categorical_feature_list])
        if self.numerical_feature_list:
            self._imputer_numerical.fit(data_df[self.numerical_feature_list])

    def _transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Transforms the data.

        Args:
            data_df (pd.DataFrame): Data to transform.

        Returns:
            pd.DataFrame: Transformed data.
        """
        data_df_transformed = data_df.copy(deep=True)

        if self.categorical_feature_list:
            data_df_transformed[self.categorical_feature_list] = self._imputer_categotical.transform(
                data_df[self.categorical_feature_list]
            )
        if self.numerical_feature_list:
            data_df_transformed[self.numerical_feature_list] = self._imputer_numerical.transform(
                data_df[self.numerical_feature_list]
            )

        return data_df_transformed

    def _inverse_transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Inverse transforms the data.

        Args:
            data_df (pd.DataFrame): Data to inverse transform.

        Returns:
            pd.DataFrame: Inverse transformed data.
        """
        data_df_inverse_transformed = data_df.copy(deep=True)

        return data_df_inverse_transformed


class CategoryTransform(BaseTransform):

    def __init__(
        self,
        categorical_feature_list: list,
        strategy: str,
    ):
        super().__init__()

        self.categorical_feature_list = categorical_feature_list
        self.strategy = strategy

        match strategy:
            case "onehot":
                # ncode categorical features as a one-hot numeric array.
                self._encoder = OneHotEncoder(sparse_output=False)
            case "ordinal":
                # This results in a single column of integers (0 to n_categories - 1) per feature.
                self._encoder = OrdinalEncoder()
            case _:
                raise ValueError(f"Invalid strategy '{strategy}'.")

    def _fit(
        self,
        data_df: pd.DataFrame,
    ):
        self._encoder.fit(data_df[self.categorical_feature_list])

    def _transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        cat_df_transformed = self._encoder.transform(data_df[self.categorical_feature_list])
        cat_df_transformed = pd.DataFrame(
            cat_df_transformed,
            columns=self._encoder.get_feature_names_out(self.categorical_feature_list),
            index=data_df.index,
        )

        data_df_transformed = data_df.drop(self.categorical_feature_list, axis=1)
        data_df_transformed = pd.concat([data_df_transformed, cat_df_transformed], axis=1)

        return data_df_transformed

    def _inverse_transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        categorical_feature_list_encoded = self._encoder.get_feature_names_out(self.categorical_feature_list)
        if len(categorical_feature_list_encoded) == 0:
            return data_df

        """One-hot encoder can inverse transform non-one-hot encoded data.
        from sklearn.preprocessing import OneHotEncoder

        enc = OneHotEncoder(handle_unknown="ignore")
        X = [["Male", 1], ["Female", 3], ["Female", 2]]
        print(enc.fit(X))
        print(enc.categories_)
        print(enc.transform([["Female", 1], ["Male", 4]]).toarray())
        print(
            enc.inverse_transform(
                [
                    [0, 1, 1, 0, 0],  # Male, 1
                    [0, 0, 0, 1, 0],  # None, 2
                    [0, 0, 0, 0, 0],  # None, None
                    [0.3, 0.7, 0.2, 0.7, 0.1],  # Male, 2
                    [0.7, 0.3, 0.2, 0.7, 0.1],  # Female, 2
                    [1, 1, 0.3, 0.3, 0.3],  # Female, 1
                ]
            )
        )
        print(enc.get_feature_names_out(["gender", "group"]))
        """
        cat_df = data_df[categorical_feature_list_encoded]
        cat_df_inverse_transformed = self._encoder.inverse_transform(cat_df)
        cat_df_inverse_transformed = pd.DataFrame(
            cat_df_inverse_transformed,
            columns=self.categorical_feature_list,
            index=data_df.index,
        )

        data_df_inverse_transformed = data_df.copy(deep=True)
        data_df_inverse_transformed = data_df_inverse_transformed.drop(categorical_feature_list_encoded, axis=1)
        data_df_inverse_transformed = pd.concat([data_df_inverse_transformed, cat_df_inverse_transformed], axis=1)

        return data_df_inverse_transformed


class TargetTransform(BaseTransform):

    def __init__(
        self,
        task: str,
        target_feature: str,
        copy: bool = True,
        with_mean: bool = True,
        with_std: bool = True,
    ):
        super().__init__()

        self.task = task
        self.target_feature = target_feature

        match task:
            case "classification":
                # The labels are sorted in alphabetic order before encoding.
                self._encoder = LabelEncoder()
            case "regression":
                self._encoder = StandardScaler(copy=copy, with_mean=with_mean, with_std=with_std)
            case _:
                raise ValueError(f"Invalid task '{task}'.")

    def _fit(
        self,
        data_df: pd.DataFrame,
    ):
        self._encoder.fit(data_df[[self.target_feature]].values.ravel())

    def _transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        data_df_transformed = data_df.copy(deep=True)
        data_df_transformed[self.target_feature] = self._encoder.transform(
            data_df[[self.target_feature]].values.ravel()
        )

        return data_df_transformed

    def _inverse_transform(
        self,
        data_df: pd.DataFrame,
    ) -> pd.DataFrame:
        data_df_inverse_transformed = data_df.copy(deep=True)
        data_df_inverse_transformed[self.target_feature] = self._encoder.inverse_transform(
            data_df[[self.target_feature]].values.ravel()
        )

        return data_df_inverse_transformed

    @property
    def encoded2class(self) -> dict:
        if self.task == "classification":
            return {i: c for i, c in enumerate(self._encoder.classes_)}

        return None
