#![allow(clippy::unused_unit)]
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use std::fs::read_to_string;


#[polars_expr(output_type=Boolean)]
fn is_tor_exit_node(inputs: &[Series]) -> PolarsResult<Series> {
    let known_exit_nodes: Vec<String> = get_tor_exit_nodes("tor_exit_nodes.txt");

    let ca: &StringChunked = inputs[0].str()?;
    let out: BooleanChunked = ca.apply_nonnull_values_generic(
        DataType::Boolean, |x| known_exit_nodes.contains(&x.to_string())
    );
    Ok(out.into_series())
}

#[polars_expr(output_type=Boolean)]
fn is_tor_node(inputs: &[Series]) -> PolarsResult<Series> {
    let known_exit_nodes: Vec<String> = get_tor_exit_nodes("tor_nodes.txt");

    let ca: &StringChunked = inputs[0].str()?;
    let out: BooleanChunked = ca.apply_nonnull_values_generic(
        DataType::Boolean, |x| known_exit_nodes.contains(&x.to_string())
    );
    Ok(out.into_series())
}


fn get_tor_exit_nodes(filename: &str) -> Vec<String> {
    let mut result = Vec::new();

    for line in read_to_string(filename).unwrap().lines() {
        result.push(line.to_string())
    }

    result
}

