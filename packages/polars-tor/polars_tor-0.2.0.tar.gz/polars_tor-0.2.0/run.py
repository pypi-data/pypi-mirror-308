import polars as pl
from polars_tor import is_tor_exit_node, is_tor_node


df = pl.DataFrame(
    {
        "ip": ["102.130.113.19", "102.130.117.167", "102.130.127.117", "103.109.101.105", "103.126.161.54", "103.163.218.11"],
    }
)
result = df.with_columns(is_tor_exit_node=is_tor_exit_node("ip"), is_tor_node=is_tor_node("ip"))
print(result)
