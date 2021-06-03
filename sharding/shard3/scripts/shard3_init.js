rs.initiate(
  {
    _id: "shard3ReplSet",
    members: [
      { _id : 0, host : "shard3svr1:27017" },
      { _id : 1, host : "shard3svr2:27017" },
      { _id : 2, host : "shard3svr3:27017" }
    ]
  }
)